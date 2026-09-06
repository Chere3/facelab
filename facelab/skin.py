"""Análisis de piel por mapas sobre una máscara de piel derivada de la malla (sin segmentación, para poder normar).

Métricas (escala-invariantes: la cara se reescala a 600 px de ancho):
- redness: media de a* (LAB) en piel relativa a la mediana, y % de píxeles con a* alto (zonas rojas)
- spots: % de piel con manchas oscuras locales (pigmentación, lesiones)
- texture: rugosidad local (std de paso alto de L) → poros y textura
- shine: % de píxeles con brillo especular (grasa)
- evenness: desviación del tono (L suavizado) sobre la piel; más alto = menos uniforme
Los mapas se guardan como superposiciones de calor sobre la cara alineada.
"""
from __future__ import annotations
from pathlib import Path
import cv2
import numpy as np
from .points import FACE_OVAL
from .geometry import align_roll

R_EYE = [33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161, 246]
L_EYE = [263, 249, 390, 373, 374, 380, 381, 382, 362, 398, 384, 385, 386, 387, 388, 466]
LIPS = [61, 146, 91, 181, 84, 17, 314, 405, 321, 375, 291, 409, 270, 269, 267, 0, 37, 39, 40, 185]
R_BROW = [70, 63, 105, 66, 107, 55, 65, 52, 53, 46]
L_BROW = [300, 293, 334, 296, 336, 285, 295, 282, 283, 276]
NOSTRILS = [98, 97, 2, 326, 327, 294, 278, 344, 440, 275, 4, 45, 220, 115, 48, 64]
TARGET_W = 600


def _poly(mask, pts, idx, val, dilate=0):
    p = np.round(pts[idx, :2]).astype(np.int32)
    cv2.fillPoly(mask, [p], val)
    if dilate:
        k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (dilate, dilate))
        sub = np.zeros_like(mask); cv2.fillPoly(sub, [p], 1); sub = cv2.dilate(sub, k)
        mask[sub > 0] = val


def skin_mask(shape_hw, pts) -> np.ndarray:
    m = np.zeros(shape_hw, np.uint8)
    _poly(m, pts, FACE_OVAL, 1)
    fh = pts[FACE_OVAL][:, 1].max() - pts[FACE_OVAL][:, 1].min()
    d = max(3, int(fh * 0.04)) | 1
    for idx in (R_EYE, L_EYE, R_BROW, L_BROW, LIPS, NOSTRILS):
        _poly(m, pts, idx, 0, dilate=d)
    # erosionar el borde del óvalo para evitar pelo/fondo
    m = cv2.erode(m, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (d, d)))
    return m


def _face_crop(img, pts):
    xy = pts[:, :2]; x0, y0, x1, y1 = xy[:, 0].min(), xy[:, 1].min(), xy[:, 0].max(), xy[:, 1].max()
    pad = 0.08 * (x1 - x0)
    x0, y0, x1, y1 = int(max(0, x0 - pad)), int(max(0, y0 - pad)), int(min(img.shape[1], x1 + pad)), int(min(img.shape[0], y1 + pad))
    crop = img[y0:y1, x0:x1]; s = TARGET_W / max(1, crop.shape[1])
    crop = cv2.resize(crop, (TARGET_W, int(crop.shape[0] * s)), interpolation=cv2.INTER_AREA)
    p = pts.copy(); p[:, 0] = (p[:, 0] - x0) * s; p[:, 1] = (p[:, 1] - y0) * s
    return crop, p


def analyze(img_bgr: np.ndarray, pts_raw: np.ndarray, out_dir: Path | None = None, stem: str | None = None) -> dict:
    from .crops import _rotate_image
    _, roll = align_roll(pts_raw)
    img, pts = _rotate_image(img_bgr, pts_raw, roll)
    face, p = _face_crop(img, pts)
    mask = skin_mask(face.shape[:2], p).astype(bool)
    if mask.sum() < 2000:
        return {"error": "máscara de piel insuficiente"}
    lab = cv2.cvtColor(face, cv2.COLOR_BGR2LAB).astype(np.float32)
    L, A, B = lab[..., 0] * (100 / 255), lab[..., 1] - 128, lab[..., 2] - 128
    Ls, As = L[mask], A[mask]

    # rojez
    a_med = float(np.median(As)); a_rel = A - a_med
    red_frac = float((a_rel[mask] > 6).mean() * 100)
    # manchas: oscurecimiento local respecto al entorno
    Lb = cv2.GaussianBlur(L, (0, 0), 12)
    dark = (Lb - L); dark[~mask] = 0
    spots = (dark > 9) & mask
    spots = cv2.morphologyEx(spots.astype(np.uint8), cv2.MORPH_OPEN, np.ones((3, 3), np.uint8)).astype(bool)
    spot_frac = float(spots.sum() / mask.sum() * 100)
    # textura / poros: paso alto y desviación local
    hp = L - cv2.GaussianBlur(L, (0, 0), 2.5)
    loc_std = np.sqrt(cv2.blur(hp * hp, (15, 15)))
    texture = float(loc_std[mask].mean())
    # brillo especular
    thr = np.percentile(Ls, 97); chroma = np.sqrt(A ** 2 + B ** 2)
    shine = ((L > max(thr, 85)) & (chroma < 18) & mask)
    shine_frac = float(shine.sum() / mask.sum() * 100)
    # uniformidad de tono
    L_smooth = cv2.GaussianBlur(L, (0, 0), 8)
    evenness = float(L_smooth[mask].std())

    res = {"redness_pct": round(red_frac, 2), "redness_a_mean": round(float(As.mean() - a_med), 2), "spots_pct": round(spot_frac, 2),
           "texture_index": round(texture, 3), "shine_pct": round(shine_frac, 2), "tone_unevenness": round(evenness, 3),
           "skin_pixels": int(mask.sum()),
           "note": "métricas relativas de esta foto (luz, maquillaje y compresión influyen); comparables solo con fotos similares"}
    if out_dir is not None and stem:
        res["maps"] = {}
        def heat(values, key, lo=None, hi=None):
            v = values.copy(); v[~mask] = np.nan
            lo = np.nanpercentile(v, 5) if lo is None else lo; hi = np.nanpercentile(v, 97) if hi is None else hi
            n = np.clip((np.nan_to_num(v, nan=lo) - lo) / (hi - lo + 1e-6), 0, 1)
            cm = cv2.applyColorMap((n * 255).astype(np.uint8), cv2.COLORMAP_INFERNO)
            out = face.copy(); out[mask] = (0.45 * face[mask] + 0.55 * cm[mask]).astype(np.uint8)
            name = f"{stem}_skin_{key}.jpg"; cv2.imwrite(str(out_dir / name), out, [cv2.IMWRITE_JPEG_QUALITY, 90]); res["maps"][key] = name
        heat(a_rel, "redness", lo=-4, hi=14)
        heat(dark, "spots", lo=0, hi=18)
        heat(loc_std, "texture")
        heat(L, "shine", lo=float(np.percentile(Ls, 50)), hi=float(np.percentile(Ls, 99)))
        m = face.copy(); m[~mask] = (m[~mask] * 0.35).astype(np.uint8)
        name = f"{stem}_skin_mask.jpg"; cv2.imwrite(str(out_dir / name), m, [cv2.IMWRITE_JPEG_QUALITY, 88]); res["maps"]["mask"] = name
    return res
