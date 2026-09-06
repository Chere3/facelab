"""Perfilometría sobre una foto lateral (≈90°).

1. face-alignment (68 pts, robusto en perfil) para anclas verticales y sentido de la cara.
2. SegFormer face-parsing para la silueta real de la cara (piel + nariz + labios + cejas + ojos; sin pelo ni orejas).
3. Puntos cefalométricos de tejido blando como extremos del contorno anterior por bandas de altura:
   trichion, glabella (G), nasion (N), pronasale (Prn), columela (Cm), subnasale (Sn), labrale superius (Ls),
   stomion (Sto), labrale inferius (Li), sublabiale (Si), pogonion (Pg), menton (Me), punto cervical (C) si hay cuello.
4. Ángulos y ratios clásicos con normas citadas.
"""
from __future__ import annotations
from functools import lru_cache
from pathlib import Path
import math
import cv2
import numpy as np

NORMS = {
    "nasofrontal": {"range": "115–135°", "source": "Powell & Humphreys 1984"},
    "nasolabial": {"range": "90–110° (M) · 95–115° (F)", "source": "Naini 2011; Powell & Humphreys"},
    "mentolabial": {"range": "120–135°", "source": "Naini 2011"},
    "facial_convexity": {"range": "165–175° (G–Sn–Pg)", "source": "Legan & Burstone 1980 (12° ± 4° de convexidad)"},
    "total_convexity": {"range": "140–150° (G–Prn–Pg)", "source": "Naini 2011"},
    "eline_upper_lip": {"range": "−4 mm (≈ −0.03 de N–Me)", "source": "Ricketts 1968"},
    "eline_lower_lip": {"range": "−2 mm (≈ −0.015 de N–Me)", "source": "Ricketts 1968"},
    "chin_projection_ratio": {"range": "−0.03 a +0.03 (Pg respecto a la vertical por Sn, / N–Me)", "source": "Legan & Burstone 0° meridian (aprox.)"},
    "nasal_projection_ratio": {"range": "0.55–0.60 (Sn–Prn / N–Prn)", "source": "Goode 1984 (adaptado a tejido blando)"},
    "submental_cervical": {"range": "90–120°", "source": "Ellenbogen & Karlin 1980"},
    "gonial_soft": {"range": "120–135° (aprox. tejido blando)", "source": "Naini 2011 (óseo 120–130°)"},
}


MAX_SIDE = 1200  # lado mayor de la foto de perfil tras reescalar


@lru_cache(maxsize=1)
def _fa():
    import face_alignment
    return face_alignment.FaceAlignment(face_alignment.LandmarksType.TWO_D, device="cpu", flip_input=False)


def _angle(a, b, c):
    v1 = np.array(a) - np.array(b); v2 = np.array(c) - np.array(b)
    return float(math.degrees(math.acos(np.clip(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2) + 1e-9), -1, 1))))


def _point_line_dist(p, a, b, sign_dir):
    """Distancia con signo de p a la recta a-b; positivo si p está hacia sign_dir (anterior)."""
    a, b, p = np.array(a, float), np.array(b, float), np.array(p, float)
    d = b - a; n = np.array([-d[1], d[0]]); n /= np.linalg.norm(n) + 1e-9
    if np.dot(n, sign_dir) < 0:
        n = -n
    return float(np.dot(p - a, n))


def analyze(image_path: str | Path, out_dir: Path | None = None, stem: str | None = None, sex: str | None = None) -> dict:
    from . import parsing
    img = cv2.imread(str(image_path))
    if img is None:
        raise ValueError("no se pudo leer la foto de perfil")
    # face-alignment en CPU sobre una foto de móvil (4000 px) tarda minutos y falla en la silueta; 1200 px basta
    scale = MAX_SIDE / max(img.shape[:2])
    if scale < 1:
        img = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
    h, w = img.shape[:2]
    lms = _fa().get_landmarks(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    if not lms:
        raise ValueError("no se detectó cara en la foto de perfil")
    lm = lms[0]
    lab = parsing.segment(img)
    I = parsing.IDX
    face = np.isin(lab, [I["skin"], I["nose"], I["u_lip"], I["l_lip"], I["mouth"], I["l_brow"], I["r_brow"], I["l_eye"], I["r_eye"], I["eye_g"]])
    neck = lab == I["neck"]
    face = cv2.morphologyEx(face.astype(np.uint8), cv2.MORPH_CLOSE, np.ones((7, 7), np.uint8)).astype(bool)
    # sentido: la punta de la nariz (30) está más lejos del centroide de la cara que el mentón
    ys, xs = np.where(face)
    cx = xs.mean()
    facing = 1 if lm[30][0] > cx else -1          # +1 = mira hacia la derecha de la imagen
    sgn = np.array([facing, 0.0])
    # contorno anterior: por fila, el x más anterior de la máscara
    ant = np.full(h, np.nan)
    for y in range(h):
        row = np.where(face[y])[0]
        if row.size:
            ant[y] = row.max() if facing > 0 else row.min()
    valid = ~np.isnan(ant)
    if valid.sum() < 50:
        raise ValueError("silueta de perfil insuficiente")
    # suavizar contorno
    ys_v = np.where(valid)[0]; xs_v = ant[valid]
    xs_s = np.convolve(np.pad(xs_v, 3, mode="edge"), np.ones(7) / 7, mode="valid")
    A = {int(y): float(x) for y, x in zip(ys_v, xs_s)}
    def most_ant(y0, y1):
        ks = [y for y in A if y0 <= y <= y1]
        if not ks: return None
        y = max(ks, key=lambda y: A[y] * facing); return (A[y], float(y))
    def most_post(y0, y1):
        ks = [y for y in A if y0 <= y <= y1]
        if not ks: return None
        y = min(ks, key=lambda y: A[y] * facing); return (A[y], float(y))
    # anclas de los 68 puntos
    y_brow = float(np.min(lm[17:27, 1])); y_nose_tip = float(lm[30][1]); y_sn = float(lm[33][1])
    y_ls = float(lm[51][1]); y_sto = float((lm[62][1] + lm[66][1]) / 2); y_li = float(lm[57][1]); y_chin = float(lm[8][1])
    y_top = int(min(A)); y_bot = int(max(A))
    P = {}
    P["trichion"] = (A[y_top], float(y_top))
    P["glabella"] = most_ant(y_top + (y_brow - y_top) * 0.5, y_brow + (y_nose_tip - y_brow) * 0.15)
    P["pronasale"] = most_ant(y_brow + (y_nose_tip - y_brow) * 0.5, y_nose_tip + (y_sn - y_nose_tip) * 0.6)
    P["nasion"] = most_post(P["glabella"][1], P["pronasale"][1] - (P["pronasale"][1] - P["glabella"][1]) * 0.3)
    P["subnasale"] = most_post(P["pronasale"][1] + 2, y_sn + (y_ls - y_sn) * 0.45)
    P["labrale_sup"] = most_ant(P["subnasale"][1] + 1, y_sto)
    P["stomion"] = most_post(y_ls + (y_sto - y_ls) * 0.4, y_sto + (y_li - y_sto) * 0.6)
    P["labrale_inf"] = most_ant(P["stomion"][1] + 1, y_li + (y_chin - y_li) * 0.35)
    P["pogonion"] = most_ant(y_li + (y_chin - y_li) * 0.5, y_chin + 4)
    P["sublabiale"] = most_post(P["labrale_inf"][1] + 1, P["pogonion"][1] - 1)
    P["menton"] = (A[y_bot], float(y_bot)) if y_bot > y_chin - 5 else (float(lm[8][0]), y_chin)
    # columela: punto del contorno a mitad entre Prn y Sn
    ym = int((P["pronasale"][1] + P["subnasale"][1]) / 2); P["columella"] = (A.get(ym, P["subnasale"][0]), float(ym))
    # gonion (tejido blando): punto del contorno mandibular (68 pts, 0–8) con mayor cambio de dirección
    jaw = lm[0:9]
    best, gidx = -1, 3
    for i in range(1, 8):
        a = _angle(jaw[i - 1], jaw[i], jaw[i + 1])
        if 180 - a > best: best, gidx = 180 - a, i
    P["gonion"] = (float(jaw[gidx][0]), float(jaw[gidx][1])); P["ramus_top"] = (float(jaw[0][0]), float(jaw[0][1]))
    # punto cervical si hay cuello
    cervical = None
    if neck.sum() > 500:
        nys, nxs = np.where(neck)
        below = nys > P["menton"][1]
        if below.sum() > 100:
            # contorno anterior del cuello; punto más posterior en la banda bajo el mentón
            cand = {}
            for y in np.unique(nys[below]):
                row = nxs[nys == y]
                cand[int(y)] = float(row.max() if facing > 0 else row.min())
            ks = sorted(cand)[: max(5, len(cand) // 2)]
            yc = min(ks, key=lambda y: cand[y] * facing); cervical = (cand[yc], float(yc)); P["cervical"] = cervical
    # medidas
    G, N, Prn, Cm, Sn, Ls, Li, Si, Pg, Me = (P[k] for k in ["glabella", "nasion", "pronasale", "columella", "subnasale", "labrale_sup", "labrale_inf", "sublabiale", "pogonion", "menton"])
    NMe = math.dist(N, Me)
    M = {
        "nasofrontal": round(_angle(G, N, Prn), 1),
        "nasolabial": round(_angle(Cm, Sn, Ls), 1),
        "mentolabial": round(_angle(Li, Si, Pg), 1),
        "facial_convexity": round(_angle(G, Sn, Pg), 1),
        "total_convexity": round(_angle(G, Prn, Pg), 1),
        "eline_upper_lip": round(_point_line_dist(Ls, Prn, Pg, sgn) / NMe, 3),
        "eline_lower_lip": round(_point_line_dist(Li, Prn, Pg, sgn) / NMe, 3),
        "chin_projection_ratio": round((Pg[0] - Sn[0]) * facing / NMe, 3),
        "nasal_projection_ratio": round(math.dist(Sn, Prn) / (math.dist(N, Prn) + 1e-9), 3),
    }
    # gonion y punto cervical no son fiables sobre silueta de tejido blando: se guardan como puntos pero no como medidas
    P.pop("ramus_top", None); P.pop("gonion", None)
    res = {"facing": "right" if facing > 0 else "left", "points": {k: [round(v[0], 1), round(v[1], 1)] for k, v in P.items()},
           "measures": {k: {"value": v, **NORMS.get(k, {})} for k, v in M.items()}, "n_me_px": round(NMe, 1),
           "warnings": ["ángulo goniaco y submental-cervical no se miden en esta versión (requieren hueso o cuello con contraste)"]}
    if out_dir is not None and stem:
        res["image"] = _draw(img, face, P, M, facing, out_dir, stem)
    return res


def _draw(img, face, P, M, facing, out_dir: Path, stem: str) -> str:
    out = img.copy()
    edge = cv2.Canny(face.astype(np.uint8) * 255, 50, 150)
    out[edge > 0] = (200, 205, 200)
    teal, ink, amber = (150, 120, 20), (30, 28, 24), (30, 160, 230)
    def L(a, b, c=teal, t=2): cv2.line(out, (int(a[0]), int(a[1])), (int(b[0]), int(b[1])), c, t, cv2.LINE_AA)
    L(P["glabella"], P["nasion"]); L(P["nasion"], P["pronasale"])
    L(P["columella"], P["subnasale"]); L(P["subnasale"], P["labrale_sup"])
    L(P["labrale_inf"], P["sublabiale"]); L(P["sublabiale"], P["pogonion"])
    L(P["pronasale"], P["pogonion"], amber, 1)  # E-line
    for k, v in P.items():
        if k == "cervical": continue
        cv2.circle(out, (int(v[0]), int(v[1])), 4, ink, -1, cv2.LINE_AA)
        cv2.putText(out, k, (int(v[0]) + 8 * facing - (60 if facing < 0 else 0), int(v[1]) + 4), cv2.FONT_HERSHEY_SIMPLEX, 0.38, ink, 1, cv2.LINE_AA)
    # recorte a la cara con margen
    ys, xs = np.where(face); x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max(); pw, ph = int((x1 - x0) * 0.35), int((y1 - y0) * 0.2)
    crop = out[max(0, y0 - ph):min(out.shape[0], y1 + ph * 2), max(0, x0 - pw):min(out.shape[1], x1 + pw)]
    name = f"{stem}_profile.jpg"; cv2.imwrite(str(out_dir / name), crop, [cv2.IMWRITE_JPEG_QUALITY, 92]); return name
