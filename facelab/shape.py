"""Forma facial: subconjunto de landmarks clave alineados por Procrustes (traslación, escala, rotación)."""
from __future__ import annotations
import numpy as np
from .points import MID, PAIRS, FACE_OVAL

# Puntos que definen la forma: línea media + pares + óvalo (sin duplicar)
KEY_IDX = sorted(set(list(MID.values()) + [i for pr in PAIRS.values() for i in pr] + FACE_OVAL))


def procrustes(xy: np.ndarray) -> np.ndarray:
    """Centra, escala a norma 1 y elimina rotación usando la línea interpupilar como referencia."""
    xy = xy - xy.mean(axis=0)
    xy = xy / (np.linalg.norm(xy) + 1e-9)
    return xy


def key_shape(pts: np.ndarray) -> np.ndarray:
    """(len(KEY_IDX), 2) forma normalizada. Se asume que pts ya viene sin roll (medidas lo alinean)."""
    from .geometry import align_roll
    aligned, _ = align_roll(pts)
    return procrustes(aligned[KEY_IDX, :2])
