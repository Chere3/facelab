"""Métricas de piel sobre MEBeauty para percentiles. uv run python -m facelab.build_skin_norms samples/mebeauty norms/mebeauty_skin.jsonl"""
from __future__ import annotations
import json, sys
from pathlib import Path
from .landmarks import detect
from .skin import analyze

MAX_POSE = 15.0


def main(root: str, out: str):
    files = [f for f in sorted((Path(root) / "original_images").rglob("*.*")) if f.suffix.lower() in (".jpg", ".jpeg", ".png")]
    n = 0
    with open(out, "w") as fh:
        for i, f in enumerate(files):
            try:
                face = detect(f)
            except Exception:
                continue
            if abs(face.yaw) > MAX_POSE or abs(face.pitch) > MAX_POSE:
                continue
            r = analyze(face.image_bgr, face.pts)
            if "error" in r:
                continue
            fh.write(json.dumps({"file": f.name, "sex": f.parts[-3], "ancestry": f.parts[-2], "skin": {k: v for k, v in r.items() if isinstance(v, (int, float))}}) + "\n"); n += 1
            if i % 300 == 0:
                print(f"{i}/{len(files)} kept={n}", flush=True)
    print("done", n)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
