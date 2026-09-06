"""Colorimetría personal y forma de cara, sin IA generativa.

- Color de piel (máscara de malla), pelo (SegFormer) e iris (landmarks 468–477) en CIELAB.
- Subtono (ángulo de matiz), profundidad (L*), croma y contraste entre pelo, piel y ojos.
- Clasificación en 12 estaciones por cercanía en tres ejes (profundidad, subtono, croma) con puntuación por estación.
- Forma de cara a partir de las medidas del informe más la anchura de sienes.
- Variantes de camisa: recolorea la prenda real de la foto (máscara "cloth") en LAB conservando textura y sombras.
Todo depende del balance de blancos y la luz de la foto: se devuelve como orientativo.
"""
from __future__ import annotations
import math
from functools import lru_cache
from pathlib import Path
import cv2
import numpy as np
import yaml

KB_PATH = Path(__file__).with_name("style.yaml")
MAX_SIDE = 1400          # análisis
BUST_MAX = 900           # imagen de busto para Codex
SHIRT_W = 520            # variantes de camisa

UNDERTONE_AXIS = {"cool": -2, "cool-neutral": -1.2, "neutral-cool": -0.6, "neutral": 0, "neutral-warm": 0.6, "warm-neutral": 1.2, "warm": 2}
DEPTH_AXIS = {"light": 1, "medium": 0, "deep": -1}
CHROMA_AXIS = {"muted": -2, "soft": -1, "medium": 0, "clear": 1, "bright": 2}


@lru_cache(maxsize=1)
def kb() -> dict:
    return yaml.safe_load(KB_PATH.read_text())


# ---------- utilidades de color ----------

def _lab_real(lab8: np.ndarray) -> np.ndarray:
    out = lab8.astype(np.float32)
    out[..., 0] *= 100 / 255; out[..., 1] -= 128; out[..., 2] -= 128
    return out


def _median_lab(lab: np.ndarray, mask: np.ndarray, lo=10, hi=90) -> np.ndarray | None:
    px = lab[mask]
    if px.shape[0] < 50:
        return None
    L = px[:, 0]; a, b = np.percentile(L, lo), np.percentile(L, hi)
    keep = (L >= a) & (L <= b)
    if keep.sum() < 20:
        keep = np.ones(len(L), bool)
    return np.median(px[keep], axis=0)


def _lab_to_hex(lab: np.ndarray) -> str:
    l8 = np.array([[[lab[0] * 255 / 100, lab[1] + 128, lab[2] + 128]]], dtype=np.float32)
    bgr = cv2.cvtColor(np.clip(l8, 0, 255).astype(np.uint8), cv2.COLOR_LAB2BGR)[0, 0]
    return "#%02x%02x%02x" % (int(bgr[2]), int(bgr[1]), int(bgr[0]))


def _hex_to_lab(hx: str) -> np.ndarray:
    hx = hx.lstrip("#"); r, g, b = int(hx[0:2], 16), int(hx[2:4], 16), int(hx[4:6], 16)
    lab8 = cv2.cvtColor(np.array([[[b, g, r]]], dtype=np.uint8), cv2.COLOR_BGR2LAB)[0, 0]
    return _lab_real(lab8.reshape(1, 1, 3))[0, 0]


def _color_entry(lab: np.ndarray | None) -> dict | None:
    if lab is None:
        return None
    L, a, b = (float(x) for x in lab)
    return {"hex": _lab_to_hex(lab), "L": round(L, 1), "a": round(a, 1), "b": round(b, 1),
            "chroma": round(math.hypot(a, b), 1), "hue": round(math.degrees(math.atan2(b, a)) % 360, 1)}


# ---------- descriptores ----------

def _undertone(skin: dict) -> tuple[str, float]:
    """Etiqueta y posición en el eje frío(-2)…cálido(+2) a partir del matiz del tono de piel."""
    h, a, c = skin["hue"], skin["a"], skin["chroma"]
    u = float(np.clip((h - 55) / 6, -2, 2))
    if h >= 62 and a < 9.5 and c <= 22:
        return "oliva", u
    if u <= -0.9: return "frío", u
    if u >= 0.9: return "cálido", u
    return "neutro", u


def _depth_label(L: float) -> str:
    return "clara" if L >= 68 else "media-clara" if L >= 60 else "media" if L >= 50 else "media-oscura" if L >= 40 else "oscura"


def _hair_label(hair: dict | None) -> str | None:
    if not hair:
        return None
    L, c, h = hair["L"], hair["chroma"], hair["hue"]
    if L < 22: return "negro"
    if L < 38: return "castaño oscuro" + (" cálido" if c > 12 and 40 < h < 80 else "")
    if L < 55: return ("cobrizo" if c > 22 and 30 < h < 70 else "castaño medio")
    if L < 70: return ("rubio oscuro" if c > 10 else "castaño claro ceniza")
    return "rubio claro" if c > 8 else "gris o blanco"


def _eye_label(eye: dict | None) -> str | None:
    if not eye:
        return None
    L, c, h = eye["L"], eye["chroma"], eye["hue"]
    if c < 7:
        return "gris" if L > 40 else "marrón muy oscuro"
    if 200 <= h <= 300: return "azul"
    if 90 < h < 200: return "verde"
    if L < 30: return "marrón oscuro"
    if L < 48: return "marrón"
    return "avellana" if c < 22 else "ámbar"


def _season_scores(depth_v: float, under_v: float, chroma_v: float) -> list[dict]:
    out = []
    for sid, s in kb()["seasons"].items():
        t = s["traits"]
        sd = 2 - min(2, abs(depth_v - DEPTH_AXIS[t["depth"]]) * 1.5)
        su = 2 - min(2, abs(under_v - UNDERTONE_AXIS[t["undertone"]]) * 0.8)
        sc = 2 - min(2, abs(chroma_v - CHROMA_AXIS[t["chroma"]]) * 0.8)
        out.append({"id": sid, "name": s["name"], "score": round(sd + su + sc, 2), "depth": round(sd, 2), "undertone": round(su, 2), "chroma": round(sc, 2)})
    return sorted(out, key=lambda x: -x["score"])


def _face_shape(report: dict, pts_xy: np.ndarray) -> dict:
    m = report.get("measures", {})
    fi = (m.get("facial_index") or {}).get("value"); jc = (m.get("jaw_to_cheek") or {}).get("value"); cw = (m.get("chin_width_to_jaw") or {}).get("value")
    temple = float(np.linalg.norm(pts_xy[127] - pts_xy[356])); zyg = float(np.linalg.norm(pts_xy[234] - pts_xy[454]))
    fc = temple / zyg if zyg else None
    scores = {k: 0.0 for k in kb()["face_shapes"]}
    if fi is not None:
        scores["oblong"] += max(0, (fi - 92) / 6); scores["round"] += max(0, (84 - fi) / 6); scores["oval"] += max(0, 1 - abs(fi - 88) / 8)
        scores["square"] += max(0, (90 - fi) / 10)
    if jc is not None:
        scores["square"] += max(0, (jc - 0.86) / 0.06); scores["triangle"] += max(0, (jc - 0.95) / 0.05); scores["round"] += max(0, (jc - 0.86) / 0.08)
        scores["heart"] += max(0, (0.84 - jc) / 0.06); scores["diamond"] += max(0, (0.84 - jc) / 0.06); scores["oval"] += max(0, 1 - abs(jc - 0.85) / 0.08)
    if cw is not None:
        scores["square"] += max(0, (cw - 0.36) / 0.06); scores["heart"] += max(0, (0.32 - cw) / 0.05); scores["round"] += max(0, (cw - 0.34) / 0.08) * 0.5
    if fc is not None:
        # las sienes de la malla casi siempre miden como los pómulos: solo pesan cuando la mandíbula ya apunta a esa forma
        if jc is None or jc < 0.87:
            scores["heart"] += max(0, (fc - 0.95) / 0.08); scores["diamond"] += max(0, (0.86 - fc) / 0.08)
        if jc is not None and jc > 0.92:
            scores["triangle"] += max(0, (0.9 - fc) / 0.08)
    best = max(scores, key=scores.get)
    if scores[best] < 0.6:
        best = "oval"
    ranked = sorted(scores.items(), key=lambda x: -x[1])
    return {"id": best, "name": kb()["face_shapes"][best]["name"], "scores": {k: round(v, 2) for k, v in ranked[:3]},
            "inputs": {"facial_index": fi, "jaw_to_cheek": jc, "chin_width_to_jaw": cw, "forehead_to_cheek": round(fc, 3) if fc else None},
            "note": "clasificación geométrica orientativa (índice facial, mandíbula/pómulos, mentón, sienes/pómulos)"}


def _hair_extent(hair: np.ndarray, pts_xy: np.ndarray) -> dict:
    if hair.sum() < 200:
        return {"visible": False}
    ys, xs = np.where(hair)
    chin = pts_xy[152][1]; eye = (pts_xy[159][1] + pts_xy[386][1]) / 2; top = pts_xy[10][1]
    fw = float(np.linalg.norm(pts_xy[234] - pts_xy[454]))
    below_chin = float((ys > chin).mean()); below_eye = float((ys > eye).mean())
    length = "largo" if below_chin > 0.12 else "medio" if below_eye > 0.15 else "corto"
    width = float(xs.max() - xs.min()) / fw if fw else None
    height_above = float(top - ys.min()) / fw if fw else None
    return {"visible": True, "length": length, "width_to_face": round(width, 2) if width else None, "height_above_forehead": round(height_above, 2) if height_above else None,
            "area_to_face": round(float(hair.sum()) / max(1.0, fw * fw), 2)}


# ---------- variantes de camisa ----------

def _recolor(img: np.ndarray, mask: np.ndarray, target_hex: str) -> np.ndarray:
    lab = _lab_real(cv2.cvtColor(img, cv2.COLOR_BGR2LAB))
    t = _hex_to_lab(target_hex)
    m = cv2.GaussianBlur(mask.astype(np.float32), (0, 0), 1.5)[..., None]
    L = lab[..., 0]; meanL = float(L[mask].mean()) if mask.any() else 50.0
    new = lab.copy()
    new[..., 0] = np.clip(L + (t[0] - meanL) * 0.9, 0, 100)
    # la saturación de la prenda original modula la del color objetivo (arrugas y sombras siguen ahí por L)
    new[..., 1] = t[1]; new[..., 2] = t[2]
    out = lab * (1 - m) + new * m
    lab8 = out.copy(); lab8[..., 0] *= 255 / 100; lab8[..., 1] += 128; lab8[..., 2] += 128
    return cv2.cvtColor(np.clip(lab8, 0, 255).astype(np.uint8), cv2.COLOR_LAB2BGR)


def _drape(img: np.ndarray, chin_y: int, target_hex: str) -> np.ndarray:
    out = img.copy(); hx = target_hex.lstrip("#"); col = (int(hx[4:6], 16), int(hx[2:4], 16), int(hx[0:2], 16))
    y0 = min(img.shape[0] - 1, int(chin_y + 0.06 * img.shape[0]))
    cv2.rectangle(out, (0, y0), (img.shape[1], img.shape[0]), col, -1)
    return out


def shirt_variants(bust: np.ndarray, cloth: np.ndarray, chin_y: int, colors: list[dict], out_dir: Path, stem: str) -> dict:
    mode = "recolor" if cloth.mean() >= 0.02 else "drape"
    scale = SHIRT_W / bust.shape[1]
    small = cv2.resize(bust, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
    msk = cv2.resize(cloth.astype(np.uint8), (small.shape[1], small.shape[0]), interpolation=cv2.INTER_NEAREST).astype(bool)
    items = []
    for i, c in enumerate(colors):
        im = _recolor(small, msk, c["hex"]) if mode == "recolor" else _drape(small, int(chin_y * scale), c["hex"])
        name = f"{stem}_shirt_{i:02d}.jpg"; cv2.imwrite(str(out_dir / name), im, [cv2.IMWRITE_JPEG_QUALITY, 88])
        items.append({**c, "file": name})
    return {"mode": mode, "cloth_fraction": round(float(cloth.mean()), 3), "items": items}


# ---------- análisis principal ----------

def analyze(img_bgr: np.ndarray, pts_raw: np.ndarray, report: dict, out_dir: Path | None = None, stem: str | None = None) -> dict:
    from .geometry import align_roll
    from .crops import _rotate_image
    from .skin import skin_mask
    from . import parsing
    _, roll = align_roll(pts_raw)
    img, pts = _rotate_image(img_bgr, pts_raw, roll)
    s = MAX_SIDE / max(img.shape[:2])
    if s < 1:
        img = cv2.resize(img, None, fx=s, fy=s, interpolation=cv2.INTER_AREA); pts = pts.copy(); pts[:, :2] *= s
    xy = pts[:, :2]
    h, w = img.shape[:2]
    lab = _lab_real(cv2.cvtColor(img, cv2.COLOR_BGR2LAB))
    seg = parsing.segment(img); I = parsing.IDX

    # piel: máscara de malla sin brillos ni sombras extremas
    skin_m = skin_mask((h, w), pts).astype(bool)
    skin = _color_entry(_median_lab(lab, skin_m, 15, 90))
    if skin is None:
        raise ValueError("máscara de piel insuficiente para colorimetría")
    # pelo
    hair_m = seg == I["hair"]
    hair = _color_entry(_median_lab(lab, hair_m, 10, 90)) if hair_m.sum() > 400 else None
    # iris: disco central de cada iris sin pupila ni brillo
    eye_px = []
    for c_idx, ring in ((468, range(469, 473)), (473, range(474, 478))):
        c = xy[c_idx]; r = float(np.mean([np.linalg.norm(xy[i] - c) for i in ring]))
        if r < 2:
            continue
        yy, xx = np.ogrid[:h, :w]
        disk = (xx - c[0]) ** 2 + (yy - c[1]) ** 2 <= (0.8 * r) ** 2
        px = lab[disk]
        if px.shape[0] < 12:
            continue
        L = px[:, 0]; keep = (L > np.percentile(L, 30)) & (L < np.percentile(L, 92))
        if keep.sum() >= 6:
            eye_px.append(px[keep])
    eyes = _color_entry(np.median(np.vstack(eye_px), axis=0)) if eye_px else None

    # ejes
    under_label, under_v = _undertone(skin)
    value = skin["L"] if hair is None else 0.45 * skin["L"] + 0.55 * hair["L"]
    depth_v = float(np.clip((value - 52) / 12, -1, 1))
    d_hair = abs(skin["L"] - hair["L"]) if hair else 0.0
    d_eye = abs(skin["L"] - eyes["L"]) if eyes else 0.0
    contrast = max(d_hair, d_eye)
    contrast_label = "alto" if contrast >= 45 else "medio" if contrast >= 25 else "bajo"
    chroma_score = 0.5 * min(1.0, (eyes["chroma"] if eyes else 8) / 20) + 0.5 * min(1.0, contrast / 60)
    chroma_v = float(np.clip((chroma_score - 0.5) * 6, -2, 2))
    chroma_label = "brillante" if chroma_v > 1.4 else "claro" if chroma_v > 0.5 else "medio" if chroma_v > -0.5 else "suave" if chroma_v > -1.4 else "apagado"

    seasons = _season_scores(depth_v, under_v, chroma_v)
    primary = kb()["seasons"][seasons[0]["id"]]
    why = [f"piel {_depth_label(skin['L'])} (L* {skin['L']}) con subtono {under_label} (matiz {skin['hue']}°, croma {skin['chroma']})"]
    if hair: why.append(f"pelo {_hair_label(hair)} (L* {hair['L']}), contraste pelo–piel {d_hair:.0f} puntos de L*")
    if eyes: why.append(f"ojos {_eye_label(eyes)} (L* {eyes['L']}, croma {eyes['chroma']})")
    why.append(f"contraste global {contrast_label}, croma {chroma_label}, profundidad de conjunto {'clara' if depth_v > 0.4 else 'oscura' if depth_v < -0.4 else 'media'}")

    res = {
        "colors": {"skin": {**skin, "depth": _depth_label(skin["L"]), "undertone": under_label}, "hair": {**hair, "label": _hair_label(hair)} if hair else None,
                   "eyes": {**eyes, "label": _eye_label(eyes)} if eyes else None},
        "axes": {"undertone": round(under_v, 2), "depth": round(depth_v, 2), "chroma": round(chroma_v, 2), "contrast_dL": round(contrast, 1)},
        "contrast": {"level": contrast_label, "rule": kb()["contrast_rules"]["high" if contrast_label == "alto" else "medium" if contrast_label == "medio" else "low"]},
        "chroma": chroma_label,
        "season": {"id": seasons[0]["id"], "name": seasons[0]["name"], "secondary": seasons[1]["name"], "secondary_id": seasons[1]["id"],
                   "margin": round(seasons[0]["score"] - seasons[1]["score"], 2), "ranking": seasons[:4], "summary": primary["summary"], "why": why},
        "palette": {k: primary[k] for k in ("best", "neutrals", "avoid", "metals", "hair_colors", "makeup", "patterns")},
        "face_shape": _face_shape(report, xy),
        "hair": _hair_extent(hair_m, xy),
        "note": "lectura de una sola foto: la luz, el balance de blancos y el maquillaje mueven el subtono y el croma; confírmala con una foto a luz de día sin filtros",
    }
    if out_dir is not None and stem:
        x0, y0, x1, y1 = xy[:, 0].min(), xy[:, 1].min(), xy[:, 0].max(), xy[:, 1].max(); fw, fh = x1 - x0, y1 - y0
        bx0, by0 = int(max(0, x0 - 1.3 * fw)), int(max(0, y0 - 0.7 * fh)); bx1, by1 = int(min(w, x1 + 1.3 * fw)), int(min(h, y1 + 1.5 * fh))
        bust = img[by0:by1, bx0:bx1]; cloth = (seg == I["cloth"])[by0:by1, bx0:bx1]
        bs = BUST_MAX / max(bust.shape[:2])
        bust_out = cv2.resize(bust, None, fx=bs, fy=bs, interpolation=cv2.INTER_AREA) if bs < 1 else bust
        bust_name = f"{stem}_bust.jpg"; cv2.imwrite(str(out_dir / bust_name), bust_out, [cv2.IMWRITE_JPEG_QUALITY, 92])
        res["bust"] = bust_name
        best_hex = {c["hex"] for c in primary["best"]}
        colors = [{**c, "group": "best"} for c in primary["best"]] + [{**c, "group": "neutral"} for c in primary["neutrals"] if c["hex"] not in best_hex][:3] + [{**c, "group": "avoid"} for c in primary["avoid"]][:3]
        res["shirts"] = shirt_variants(bust, cloth, int(y1 - by0), colors, out_dir, stem)
    return res
