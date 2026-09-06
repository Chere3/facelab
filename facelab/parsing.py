"""Segmentación semántica de la cara (SegFormer face-parsing): línea del pelo real, orejas, cuello, pelo."""
from __future__ import annotations
from functools import lru_cache
import numpy as np
import cv2

# id2label del modelo jonathandinu/face-parsing (CelebAMask-HQ)
LABELS = {0: "background", 1: "skin", 2: "nose", 3: "eye_g", 4: "l_eye", 5: "r_eye", 6: "l_brow", 7: "r_brow", 8: "l_ear", 9: "r_ear",
          10: "mouth", 11: "u_lip", 12: "l_lip", 13: "hair", 14: "hat", 15: "ear_r", 16: "neck_l", 17: "neck", 18: "cloth"}
IDX = {v: k for k, v in LABELS.items()}


@lru_cache(maxsize=1)
def _model():
    from transformers import SegformerImageProcessor, SegformerForSemanticSegmentation
    proc = SegformerImageProcessor.from_pretrained("jonathandinu/face-parsing")
    model = SegformerForSemanticSegmentation.from_pretrained("jonathandinu/face-parsing").eval()
    return proc, model


def segment(img_bgr: np.ndarray) -> np.ndarray:
    import torch
    from PIL import Image
    proc, model = _model()
    img = Image.fromarray(cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB))
    with torch.no_grad():
        logits = model(**proc(images=img, return_tensors="pt")).logits
    lab = torch.nn.functional.interpolate(logits, size=img.size[::-1], mode="bilinear", align_corners=False).argmax(1)[0]
    return lab.numpy().astype(np.uint8)


def analyze(img_bgr: np.ndarray, pts: np.ndarray) -> dict:
    """Devuelve trichion real, tercios corregidos, visibilidad de orejas, gafas, y máscaras resumidas."""
    from .points import P
    lab = segment(img_bgr)
    p = P(pts)
    gl, sn, me = p.mid("glabella"), p.mid("subnasale"), p.mid("menton")
    x = int(gl[0]); h = lab.shape[0]
    # trichion: primer píxel de piel bajando por la columna de la glabella desde arriba (bajo pelo/gorro)
    col = lab[:, max(0, x - 3):x + 4]
    skin_rows = np.where((col == IDX["skin"]).any(axis=1))[0]
    skin_rows = skin_rows[skin_rows < gl[1]]
    trichion_y = int(skin_rows.min()) if skin_rows.size else None
    res = {"trichion_y": trichion_y, "hair_visible": bool((lab == IDX["hair"]).mean() > 0.005),
           "hat": bool((lab == IDX["hat"]).mean() > 0.005), "glasses": bool((lab == IDX["eye_g"]).mean() > 0.002),
           "ear_visible": {"R": bool((lab == IDX["l_ear"]).sum() > 200 or (lab == IDX["r_ear"]).sum() > 200)},
           "neck_visible": bool((lab == IDX["neck"]).mean() > 0.01)}
    ears = ((lab == IDX["l_ear"]) | (lab == IDX["r_ear"]))
    res["ear_visible"] = {"any": bool(ears.sum() > 200), "area_px": int(ears.sum())}
    if trichion_y is not None and trichion_y < gl[1] - 5:
        upper = float(gl[1] - trichion_y); middle = float(sn[1] - gl[1]); lower = float(me[1] - sn[1]); tot = upper + middle + lower
        res["facial_thirds_true"] = {"upper": round(upper / tot, 3), "middle": round(middle / tot, 3), "lower": round(lower / tot, 3),
                                     "note": "tercio superior medido hasta la línea del pelo real (segmentación), no al proxy de la malla"}
        res["forehead_height_px"] = round(upper, 1)
    return res


def overlay(img_bgr: np.ndarray, lab: np.ndarray) -> np.ndarray:
    """Superposición de color suave por región (para el informe)."""
    palette = np.zeros((19, 3), dtype=np.uint8)
    palette[IDX["skin"]] = (60, 140, 220); palette[IDX["hair"]] = (120, 60, 20); palette[IDX["nose"]] = (20, 160, 200)
    palette[IDX["l_eye"]] = palette[IDX["r_eye"]] = (200, 80, 40); palette[IDX["l_brow"]] = palette[IDX["r_brow"]] = (80, 40, 160)
    palette[IDX["u_lip"]] = palette[IDX["l_lip"]] = (40, 40, 200); palette[IDX["mouth"]] = (80, 80, 240)
    palette[IDX["l_ear"]] = palette[IDX["r_ear"]] = (30, 200, 120); palette[IDX["neck"]] = (150, 180, 90)
    color = palette[lab]
    mask = (lab > 0)[..., None]
    return np.where(mask, (0.55 * img_bgr + 0.45 * color).astype(np.uint8), img_bgr)
