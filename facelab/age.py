"""Edad y sexo aparentes con InsightFace (buffalo_l, CPU). Orientativo: error típico ±6-8 años."""
from __future__ import annotations
from functools import lru_cache
import numpy as np


@lru_cache(maxsize=1)
def _app():
    from insightface.app import FaceAnalysis
    app = FaceAnalysis(name="buffalo_l", providers=["CPUExecutionProvider"], allowed_modules=["detection", "genderage"])
    app.prepare(ctx_id=0, det_size=(640, 640))
    return app


def estimate(img_bgr: np.ndarray) -> dict | None:
    faces = _app().get(img_bgr)
    if not faces:
        return None
    f = max(faces, key=lambda x: (x.bbox[2] - x.bbox[0]) * (x.bbox[3] - x.bbox[1]))
    return {"visual_age": int(f.age), "apparent_sex": "male" if int(f.gender) == 1 else "female",
            "note": "estimación de un modelo de edad aparente (InsightFace); error típico ±6–8 años, sensible a luz y expresión"}
