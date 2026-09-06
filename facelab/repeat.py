"""Repetibilidad sobre FEI: misma persona, varias fotos frontales (11, 13, 14 = neutra con distinta luz/toma).

Uso: uv run python -m facelab.repeat samples/fei out/fei_repeat.json
Imprime CV% (desviación típica / media) por medida escalar, mediana entre sujetos, y el yaw estimado por pose.
"""
from __future__ import annotations
import json, sys, statistics as st
from collections import defaultdict
from pathlib import Path
from .landmarks import detect
from .measures import compute

FRONTAL_POSES = ["11", "13", "14"]


from .measures import CATALOG_BY_ID


def is_degrees(key: str) -> bool:
    return CATALOG_BY_ID.get(key.split(".")[0], {}).get("unit") == "deg"


def flat(measures: dict) -> dict[str, float]:
    out = {}
    for k, v in measures.items():
        val = v["value"]
        if isinstance(val, dict):
            for kk, vv in val.items():
                if isinstance(vv, (int, float)):
                    out[f"{k}.{kk}"] = vv
        elif isinstance(val, (int, float)):
            out[k] = val
    return out


def main(root: str, out: str):
    root = Path(root)
    subjects = sorted({p.name.split("-")[0] for p in root.glob("*.jpg")}, key=int)
    yaw_by_pose = defaultdict(list)
    cv_by_measure = defaultdict(list)
    sd_deg_by_measure = defaultdict(list)
    failures = []
    for s in subjects:
        runs = []
        for pose in [f"{i:02d}" for i in range(1, 15)]:
            f = root / f"{s}-{pose}.jpg"
            if not f.exists():
                continue
            try:
                face = detect(f)
            except Exception as e:
                failures.append((f.name, str(e))); continue
            yaw_by_pose[pose].append(face.yaw)
            if pose in FRONTAL_POSES:
                runs.append(flat(compute(face.pts)["measures"]))
        if len(runs) >= 2:
            for k in runs[0]:
                vals = [r[k] for r in runs if k in r and r[k] is not None]
                if len(vals) < 2:
                    continue
                if is_degrees(k):
                    sd_deg_by_measure[k].append(st.pstdev(vals))
                elif abs(st.mean(vals)) > 1e-6:
                    cv_by_measure[k].append(abs(st.pstdev(vals) / st.mean(vals)) * 100)
    summary = {
        "subjects": len(subjects),
        "failures": failures,
        "yaw_deg_by_pose_median": {p: round(st.median(v), 1) for p, v in sorted(yaw_by_pose.items())},
        "detections_by_pose": {p: len(v) for p, v in sorted(yaw_by_pose.items())},
        "cv_pct_median_by_measure": {k: round(st.median(v), 2) for k, v in sorted(cv_by_measure.items(), key=lambda kv: st.median(kv[1]))},
        "sd_deg_median_by_measure": {k: round(st.median(v), 2) for k, v in sorted(sd_deg_by_measure.items(), key=lambda kv: st.median(kv[1]))},
    }
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    Path(out).write_text(json.dumps(summary, indent=2, ensure_ascii=False))
    print(f"sujetos: {summary['subjects']}  fallos: {len(failures)}")
    print("yaw mediano por pose:", summary["yaw_deg_by_pose_median"])
    print("detecciones por pose:", summary["detections_by_pose"])
    print(f"\n{'medida':34s} CV% mediano (3 fotos frontales)")
    for k, v in summary["cv_pct_median_by_measure"].items():
        flag = "" if v < 3 else ("  <- >3%" if v < 8 else "  <- >8% (inestable)")
        print(f"{k:34s} {v:6.2f}{flag}")
    print(f"\n{'ángulo':34s} SD mediana en grados (3 fotos frontales)")
    for k, v in summary["sd_deg_median_by_measure"].items():
        flag = "" if v < 1.5 else ("  <- >1.5°" if v < 3 else "  <- >3° (inestable)")
        print(f"{k:34s} {v:6.2f}{flag}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
