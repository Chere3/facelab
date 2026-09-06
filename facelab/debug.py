"""Dibuja landmarks y líneas de medida sobre la foto para inspección visual."""
from __future__ import annotations
import cv2
import numpy as np
from .points import P, MID, PAIRS


def draw(img: np.ndarray, pts: np.ndarray) -> np.ndarray:
    out = img.copy()
    for x, y, _ in pts:
        cv2.circle(out, (int(x), int(y)), 1, (90, 90, 90), -1, cv2.LINE_AA)
    p = P(pts)
    teal, amber, red = (150, 120, 20), (30, 160, 230), (60, 60, 220)
    for name in MID:
        x, y, _ = p.mid(name)
        cv2.circle(out, (int(x), int(y)), 4, amber, -1, cv2.LINE_AA)
        cv2.putText(out, name, (int(x) + 6, int(y) + 4), cv2.FONT_HERSHEY_SIMPLEX, 0.38, amber, 1, cv2.LINE_AA)
    for name in PAIRS:
        for q in p.pair(name):
            cv2.circle(out, (int(q[0]), int(q[1])), 4, teal, -1, cv2.LINE_AA)
    for q in p.alare():
        cv2.circle(out, (int(q[0]), int(q[1])), 4, red, -1, cv2.LINE_AA)
    line = lambda a, b, c: cv2.line(out, (int(a[0]), int(a[1])), (int(b[0]), int(b[1])), c, 1, cv2.LINE_AA)
    line(*p.pair("zygion"), teal); line(*p.pair("gonion"), teal); line(*p.pair("pupil"), teal)
    line(*p.pair("cheilion"), teal); line(*p.alare(), red)
    line(p.mid("nasion"), p.mid("menton"), amber); line(p.mid("glabella"), p.mid("subnasale"), amber)
    return out
