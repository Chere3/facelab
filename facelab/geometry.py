"""Utilidades geométricas: alineación por roll, distancias, ángulos, simetría."""
from __future__ import annotations
import math
import numpy as np
from .points import P, PAIRS


def dist(a, b) -> float:
    return float(np.hypot(a[0] - b[0], a[1] - b[1]))


def angle_deg(a, b, c) -> float:
    """Ángulo en b formado por a-b-c (plano XY), en grados."""
    v1 = np.array([a[0] - b[0], a[1] - b[1]])
    v2 = np.array([c[0] - b[0], c[1] - b[1]])
    cosang = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2) + 1e-9)
    return float(math.degrees(math.acos(np.clip(cosang, -1, 1))))


def angle_deg_3d(a, b, c, axes=(0, 1, 2)) -> float:
    v1 = np.array([a[i] - b[i] for i in axes])
    v2 = np.array([c[i] - b[i] for i in axes])
    cosang = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2) + 1e-9)
    return float(math.degrees(math.acos(np.clip(cosang, -1, 1))))


def align_roll(pts: np.ndarray) -> tuple[np.ndarray, float]:
    """Rota los puntos para que la línea interpupilar quede horizontal. Devuelve (pts, roll_aplicado)."""
    p = P(pts)
    r, l = p.pair("pupil")
    roll = math.degrees(math.atan2(l[1] - r[1], l[0] - r[0]))
    c = (r + l) / 2
    th = math.radians(-roll)
    rot = np.array([[math.cos(th), -math.sin(th)], [math.sin(th), math.cos(th)]])
    out = pts.copy()
    out[:, :2] = (pts[:, :2] - c[:2]) @ rot.T + c[:2]
    return out, roll


def midline_x(pts: np.ndarray) -> float:
    p = P(pts)
    r, l = p.pair("pupil")
    return float((r[0] + l[0]) / 2)


def symmetry(pts: np.ndarray, face_height: float) -> dict:
    """Asimetría bilateral sobre pares nombrados, tras alinear roll.

    Para cada par (R, L) mide cuánto se desvía L del reflejo de R sobre la línea media
    definida por las pupilas. Devuelve error medio normalizado por altura facial y un
    score 0-100 (100 = perfectamente simétrico). No es una norma clínica; es un índice interno.
    """
    p = P(pts)
    mx = midline_x(pts)
    errs = {}
    for name in PAIRS:
        r, l = p.pair(name)
        mirror_x = 2 * mx - r[0]
        dx = abs(l[0] - mirror_x)
        dy = abs(l[1] - r[1])
        errs[name] = float(np.hypot(dx, dy) / face_height * 100)
    mean_err = float(np.mean(list(errs.values())))
    score = max(0.0, 100.0 - mean_err * 10.0)
    return {"mean_error_pct_face_height": round(mean_err, 3), "score": round(score, 1),
            "per_landmark_pct": {k: round(v, 3) for k, v in errs.items()}}
