"""CLI:
  uv run python -m facelab analyze foto.jpg [-o salida.json] [--debug salida.jpg] [--sex male|female]
                                [--ancestry asian|black|caucasian|hispanic|indian|mideastern|other] [--age N] [--narrate]
"""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
import cv2
from . import __version__
from .landmarks import detect, FaceResult
from .measures import compute
from .debug import draw
from .profile import Profile, SEXES, ANCESTRIES
from .repeat import flat
from .shape import key_shape

POSE_LIMITS = {"yaw": 12.0, "pitch": 12.0}


def build_report(path: str, profile: Profile | None = None) -> tuple[dict, FaceResult]:
    from .norms import get_norms
    face = detect(path)
    quality = {"yaw_deg": round(face.yaw, 1), "pitch_deg": round(face.pitch, 1), "roll_deg": round(face.roll, 1),
               "blur_laplacian_var": round(face.blur, 1), "width": face.size[0], "height": face.size[1]}
    warnings = []
    if abs(face.yaw) > POSE_LIMITS["yaw"]:
        warnings.append(f"yaw {face.yaw:.1f}° supera ±{POSE_LIMITS['yaw']}°: las medidas frontales no son fiables")
    if abs(face.pitch) > POSE_LIMITS["pitch"]:
        warnings.append(f"pitch {face.pitch:.1f}° supera ±{POSE_LIMITS['pitch']}°: proporciones verticales distorsionadas")
    if face.blur < 60:
        warnings.append(f"imagen borrosa (var. laplaciano {face.blur:.0f} < 60)")
    profile = profile or Profile()
    measures = compute(face.pts)
    if (measures["measures"]["commissure_tilt"]["value"] or 0) > 8:
        warnings.append("posible sonrisa (comisuras muy elevadas): boca, labios y proporcionalidad quedan distorsionados; repite con la boca en reposo")
    report = {"facelab_version": __version__, "source": str(path), "profile": profile.to_dict(),
              "quality": quality, "warnings": warnings}
    report.update(measures)
    fm = flat(report["measures"])
    norms = get_norms()
    if norms.rows:
        sex, anc = profile.norm_keys()
        shape = key_shape(face.pts)
        report["shape"] = shape.round(5).tolist()
        report["norms"] = norms.enrich(fm, sex, anc)
        report["scores"] = {
            "symmetry": {"score": report["measures"]["symmetry"]["value"], **norms.symmetry_percentile(report["measures"]["symmetry"]["value"], sex, anc)},
            "averageness": norms.averageness(shape, sex, anc),
            "dimorphism": norms.dimorphism(shape, sex, anc),
            "proportionality": norms.proportionality(fm, sex, anc),
        }
        report["dataset_correlations"] = norms.attractiveness_correlations(sex, anc)
    else:
        warnings.append("sin normas: ejecuta facelab.build_norms")
    return report, face


def enrich_visual(report: dict, face, out: str | None, full: bool = True) -> None:
    """Recortes, edad visual y segmentación (línea del pelo, orejas). Escribe imágenes junto al JSON."""
    if not out:
        return
    out_dir, stem = Path(out).parent, Path(out).stem
    from .crops import make_crops
    report["assets"] = make_crops(face.image_bgr, face.pts, out_dir, stem)
    if not full:
        return
    try:
        from .age import estimate
        report["age"] = estimate(face.image_bgr)
    except Exception as e:
        report.setdefault("warnings", []).append(f"edad visual no disponible: {e}")
    try:
        from .skin import analyze as skin_analyze
        from .norms import get_norms
        report["skin"] = skin_analyze(face.image_bgr, face.pts, out_dir, stem)
        sex, anc = Profile(**report.get("profile", {})).norm_keys()
        report["skin"]["percentiles"] = get_norms().skin_percentiles(report["skin"], sex, anc)
    except Exception as e:
        report.setdefault("warnings", []).append(f"análisis de piel no disponible: {e}")
    try:
        from . import parsing
        lab = parsing.segment(face.image_bgr)
        report["parsing"] = parsing.analyze(face.image_bgr, face.pts)
        name = f"{stem}_parsing.jpg"
        cv2.imwrite(str(out_dir / name), parsing.overlay(face.image_bgr, lab), [cv2.IMWRITE_JPEG_QUALITY, 90])
        report["assets"]["parsing"] = name
        if report["parsing"].get("facial_thirds_true"):
            report["measures"]["facial_thirds"]["true"] = report["parsing"]["facial_thirds_true"]
    except Exception as e:
        report.setdefault("warnings", []).append(f"segmentación no disponible: {e}")


def analyze(path: str, out: str | None, debug: str | None, force: bool = True, profile: Profile | None = None,
            narrate: bool = False, protocol: bool = False, visual: bool = True) -> dict:
    report, face = build_report(path, profile)
    if report["warnings"] and not force:
        print("AVISO:", *report["warnings"], sep="\n  ", file=sys.stderr)
    enrich_visual(report, face, out, full=visual)
    if narrate:
        from .narrate import narrate as _narrate
        report["narrative"] = _narrate(report)
    if protocol:
        from .protocol import build as _protocol
        report["protocol"] = _protocol(report)
    if out:
        Path(out).parent.mkdir(parents=True, exist_ok=True)
        Path(out).write_text(json.dumps(report, indent=2, ensure_ascii=False))
    if debug:
        Path(debug).parent.mkdir(parents=True, exist_ok=True)
        cv2.imwrite(debug, draw(face.image_bgr, face.pts))
    return report


def main():
    ap = argparse.ArgumentParser(prog="facelab")
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("analyze", help="analiza una foto frontal")
    a.add_argument("image"); a.add_argument("-o", "--out"); a.add_argument("--debug"); a.add_argument("--force", action="store_true")
    a.add_argument("--sex", choices=SEXES); a.add_argument("--ancestry", choices=ANCESTRIES); a.add_argument("--age", type=int)
    a.add_argument("--narrate", action="store_true", help="redacta la narrativa por sección con Claude")
    a.add_argument("--protocol", action="store_true", help="genera el protocolo no quirúrgico con Claude")
    a.add_argument("--no-visual", action="store_true", help="omite edad visual y segmentación (más rápido)")
    args = ap.parse_args()
    if args.cmd == "analyze":
        prof = Profile(sex=args.sex, ancestry=args.ancestry, age=args.age)
        res = analyze(args.image, args.out, args.debug, args.force, prof, args.narrate, args.protocol, not args.no_visual)
        if not args.out:
            print(json.dumps(res, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
