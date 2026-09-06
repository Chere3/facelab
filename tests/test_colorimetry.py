"""Tests ligeros de colorimetría: no cargan modelos (MediaPipe, SegFormer), solo la lógica de clasificación."""
from __future__ import annotations
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from facelab import colorimetry as C  # noqa: E402


def test_kb_loads_all_seasons_and_shapes():
    kb = C.kb()
    assert len(kb["seasons"]) == 12
    assert len(kb["face_shapes"]) == 7
    for sid, s in kb["seasons"].items():
        assert s["traits"]["depth"] in C.DEPTH_AXIS, sid
        assert s["traits"]["undertone"] in C.UNDERTONE_AXIS, sid
        assert s["traits"]["chroma"] in C.CHROMA_AXIS, sid
        assert len(s["best"]) >= 8 and all(c["hex"].startswith("#") for c in s["best"])


def test_season_scores_deep_warm_picks_deep_autumn():
    ranking = C._season_scores(depth_v=-1.0, under_v=1.2, chroma_v=0.0)
    assert ranking[0]["id"] == "otono_profundo"
    assert ranking[0]["score"] > ranking[1]["score"]


def test_season_scores_light_cool_soft_picks_light_summer():
    ranking = C._season_scores(depth_v=1.0, under_v=-1.2, chroma_v=-1.0)
    assert ranking[0]["id"] == "verano_claro"


def test_hex_lab_roundtrip():
    for hx in ("#000000", "#ffffff", "#6d4cff", "#b7410e"):
        lab = C._hex_to_lab(hx)
        back = C._lab_to_hex(lab)
        r0, g0, b0 = (int(hx[i:i + 2], 16) for i in (1, 3, 5))
        r1, g1, b1 = (int(back[i:i + 2], 16) for i in (1, 3, 5))
        assert max(abs(r0 - r1), abs(g0 - g1), abs(b0 - b1)) <= 3


def test_undertone_labels():
    warm = {"hue": 66.0, "a": 12.0, "chroma": 24.0}
    cool = {"hue": 44.0, "a": 16.0, "chroma": 20.0}
    neutral = {"hue": 55.0, "a": 11.0, "chroma": 18.0}
    assert C._undertone(warm)[0] == "cálido"
    assert C._undertone(cool)[0] == "frío"
    assert C._undertone(neutral)[0] == "neutro"


def _pts(temple_ratio: float) -> np.ndarray:
    """Malla mínima: solo los índices que usa _face_shape (sienes 127/356, pómulos 234/454)."""
    pts = np.zeros((478, 2))
    pts[234], pts[454] = (0.0, 0.0), (100.0, 0.0)
    pts[127], pts[356] = (50 - 50 * temple_ratio, -20.0), (50 + 50 * temple_ratio, -20.0)
    return pts


def test_face_shape_square_and_oblong():
    square = {"measures": {"facial_index": {"value": 80.0}, "jaw_to_cheek": {"value": 0.95}, "chin_width_to_jaw": {"value": 0.42}}}
    assert C._face_shape(square, _pts(0.95))["id"] == "square"
    oblong = {"measures": {"facial_index": {"value": 100.0}, "jaw_to_cheek": {"value": 0.85}, "chin_width_to_jaw": {"value": 0.34}}}
    assert C._face_shape(oblong, _pts(0.95))["id"] == "oblong"


def test_recolor_keeps_shading_and_changes_hue():
    img = np.full((40, 40, 3), 120, np.uint8)
    img[:, :20] = 60  # mitad más oscura: la sombra debe sobrevivir
    mask = np.ones((40, 40), bool)
    out = C._recolor(img, mask, "#b7410e")  # óxido
    b, g, r = (out[..., i].astype(float) for i in range(3))
    assert r.mean() > b.mean()  # cambió el matiz hacia rojo-naranja
    assert out[:, :20].mean() < out[:, 20:].mean()  # la mitad oscura sigue más oscura
