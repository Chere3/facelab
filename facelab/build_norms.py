"""Paso 1 de normas: extrae medidas y forma normalizada de cada imagen de MEBeauty.

uv run python -m facelab.build_norms samples/mebeauty norms/mebeauty_features.jsonl
Salida: una línea JSON por imagen con sexo, ascendencia, score de atractivo, pose, medidas planas
y la forma (landmarks clave alineados por Procrustes, sin escala ni rotación).
"""
from __future__ import annotations
import json, sys, csv
from pathlib import Path
from .landmarks import detect
from .measures import compute
from .repeat import flat
from .shape import key_shape

MAX_YAW, MAX_PITCH = 15.0, 15.0


def load_scores(root: Path) -> dict[str, float]:
    scores = {}
    for f in ["train_universal_scores.csv", "test_universal_scores.csv"]:
        p = root / "scores" / f
        if p.exists():
            with open(p) as fh:
                for row in csv.DictReader(fh):
                    scores[Path(row["image"]).name] = float(row["score"])
    return scores


def main(root: str, out: str):
    root = Path(root)
    scores = load_scores(root)
    files = sorted((root / "original_images").rglob("*.*"))
    files = [f for f in files if f.suffix.lower() in (".jpg", ".jpeg", ".png")]
    kept = skipped = failed = 0
    with open(out, "w") as fh:
        for i, f in enumerate(files):
            sex, ancestry = f.parts[-3], f.parts[-2]
            try:
                face = detect(f)
            except Exception:
                failed += 1; continue
            if abs(face.yaw) > MAX_YAW or abs(face.pitch) > MAX_PITCH:
                skipped += 1; continue
            res = compute(face.pts)
            rec = {"file": f.name, "sex": sex, "ancestry": ancestry, "score": scores.get(f.name),
                   "yaw": round(face.yaw, 1), "pitch": round(face.pitch, 1),
                   "measures": flat(res["measures"]), "shape": key_shape(face.pts).round(4).tolist()}
            fh.write(json.dumps(rec) + "\n"); kept += 1
            if i % 200 == 0:
                print(f"{i}/{len(files)} kept={kept} skipped_pose={skipped} failed={failed}", flush=True)
    print(f"done: kept={kept} skipped_pose={skipped} failed={failed} -> {out}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
