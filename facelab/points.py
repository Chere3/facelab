"""Landmarks antropométricos nombrados sobre la malla de 478 puntos de MediaPipe.

Convención: "R"/"L" son el lado DEL SUJETO en una foto no espejada (su derecha queda
a la izquierda de la imagen). Los índices vienen de la topología canónica de Face Mesh.
"""
from __future__ import annotations
import numpy as np

# Puntos únicos (línea media)
MID = {
    "forehead_top": 10,     # punto más alto de la malla; proxy de trichion (NO es la línea del pelo)
    "glabella": 9,
    "nasion": 168,          # sellion de tejido blando
    "pronasale": 1,         # punta nasal
    "subnasale": 2,
    "labiale_superius": 0,
    "stomion_sup": 13,
    "stomion_inf": 14,
    "labiale_inferius": 17,
    "sublabiale": 18,       # surco mentolabial
    "pogonion": 199,
    "menton": 152,
}

# Pares (derecha del sujeto, izquierda del sujeto)
PAIRS = {
    "exocanthion": (33, 263),
    "endocanthion": (133, 362),
    "eyelid_sup": (159, 386),
    "eyelid_inf": (145, 374),
    "pupil": (468, 473),
    "brow_head": (107, 336),
    "brow_apex": (105, 334),
    "brow_tail": (70, 300),
    "brow_mid_low": (66, 296),
    "cupid_peak": (37, 267),
    "cheilion": (61, 291),
    "zygion": (234, 454),   # punto más ancho del óvalo a la altura del trago
    "gonion": (58, 288),
    "chin_lat": (176, 400),
    "temple": (127, 356),
    "jaw_mid": (172, 397),
}

ALA_R = [49, 64, 98, 129, 131]
ALA_L = [279, 294, 327, 358, 360]

FACE_OVAL = [10, 338, 297, 332, 284, 251, 389, 356, 454, 323, 361, 288, 397, 365, 379, 378, 400, 377,
             152, 148, 176, 149, 150, 136, 172, 58, 132, 93, 234, 127, 162, 21, 54, 103, 67, 109]


class P:
    """Acceso cómodo: P(pts).mid('nasion') -> (x, y, z); P(pts).pair('pupil') -> (R, L)."""

    def __init__(self, pts: np.ndarray):
        self.pts = pts

    def mid(self, name: str) -> np.ndarray:
        return self.pts[MID[name]]

    def pair(self, name: str) -> tuple[np.ndarray, np.ndarray]:
        r, l = PAIRS[name]
        return self.pts[r], self.pts[l]

    def alare(self) -> tuple[np.ndarray, np.ndarray]:
        r = self.pts[ALA_R][np.argmin(self.pts[ALA_R][:, 0])]
        l = self.pts[ALA_L][np.argmax(self.pts[ALA_L][:, 0])]
        return r, l

    def oval(self) -> np.ndarray:
        return self.pts[FACE_OVAL]
