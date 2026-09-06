"""Recortes y composiciones fotográficas para el informe: cara alineada, zonas, espejos de simetría y malla."""
from __future__ import annotations
from pathlib import Path
import cv2
import numpy as np
from .points import P, PAIRS, MID, FACE_OVAL
from .geometry import align_roll

INK = (30, 28, 24); ACCENT = (150, 120, 20); SOFT = (200, 205, 200)


def _rotate_image(img: np.ndarray, pts: np.ndarray, roll: float) -> tuple[np.ndarray, np.ndarray]:
    """Gira la imagen para que la línea interpupilar quede horizontal; devuelve imagen y puntos girados."""
    p = P(pts); r, l = p.pair("pupil"); c = ((r[0] + l[0]) / 2, (r[1] + l[1]) / 2)
    M = cv2.getRotationMatrix2D(c, roll, 1.0)
    h, w = img.shape[:2]
    out = cv2.warpAffine(img, M, (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
    xy = np.hstack([pts[:, :2], np.ones((len(pts), 1))]) @ M.T
    npts = pts.copy(); npts[:, :2] = xy
    return out, npts


def _crop(img, x0, y0, x1, y1, pad=0.0, square=False):
    h, w = img.shape[:2]
    cw, ch = x1 - x0, y1 - y0
    x0 -= cw * pad; x1 += cw * pad; y0 -= ch * pad; y1 += ch * pad
    if square:
        s = max(x1 - x0, y1 - y0); cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        x0, x1, y0, y1 = cx - s / 2, cx + s / 2, cy - s / 2, cy + s / 2
    x0, y0 = int(max(0, x0)), int(max(0, y0)); x1, y1 = int(min(w, x1)), int(min(h, y1))
    return img[y0:y1, x0:x1].copy(), (x0, y0)


def _bbox(pts_xy):
    return pts_xy[:, 0].min(), pts_xy[:, 1].min(), pts_xy[:, 0].max(), pts_xy[:, 1].max()


def _draw_points(img, pts_xy, offset, color=ACCENT, r=None, labels=None):
    r = r or max(2, int(img.shape[1] / 220))
    for i, (x, y) in enumerate(pts_xy):
        cv2.circle(img, (int(x - offset[0]), int(y - offset[1])), r, color, -1, cv2.LINE_AA)
        if labels:
            cv2.putText(img, labels[i], (int(x - offset[0]) + 6, int(y - offset[1]) - 4), cv2.FONT_HERSHEY_SIMPLEX, 0.4, color, 1, cv2.LINE_AA)


def _line(img, a, b, offset, color=ACCENT, t=None):
    t = t or max(1, int(img.shape[1] / 500))
    cv2.line(img, (int(a[0] - offset[0]), int(a[1] - offset[1])), (int(b[0] - offset[0]), int(b[1] - offset[1])), color, t, cv2.LINE_AA)


def _upscale(img, min_w=700):
    h, w = img.shape[:2]
    if w < min_w:
        s = min_w / w
        img = cv2.resize(img, (int(w * s), int(h * s)), interpolation=cv2.INTER_CUBIC)
    return img


def make_crops(img: np.ndarray, pts_raw: np.ndarray, out_dir: Path, stem: str) -> dict[str, str]:
    """Genera los recortes y devuelve {clave: nombre_de_archivo}."""
    _, roll = align_roll(pts_raw)
    img, pts = _rotate_image(img, pts_raw, roll)
    p = P(pts); xy = pts[:, :2]
    out: dict[str, str] = {}

    def save(key, im):
        name = f"{stem}_{key}.jpg"; cv2.imwrite(str(out_dir / name), _upscale(im), [cv2.IMWRITE_JPEG_QUALITY, 92]); out[key] = name

    # cara alineada con margen
    x0, y0, x1, y1 = _bbox(xy); fh = y1 - y0
    face, off = _crop(img, x0, y0 - fh * 0.35, x1, y1 + fh * 0.08, pad=0.12, square=True)
    save("face", face)

    # malla completa sobre la cara
    mesh = face.copy()
    for x, y in xy:
        cv2.circle(mesh, (int(x - off[0]), int(y - off[1])), 1, SOFT, -1, cv2.LINE_AA)
    for name in PAIRS:
        _draw_points(mesh, np.array([q[:2] for q in p.pair(name)]), off, ACCENT)
    for name in MID:
        _draw_points(mesh, np.array([p.mid(name)[:2]]), off, INK)
    save("mesh", mesh)

    # tercios y quintos sobre la cara
    guides = face.copy()
    for name in ["glabella", "subnasale", "menton", "forehead_top"]:
        y = p.mid(name)[1]; _line(guides, (x0 - 40, y), (x1 + 40, y), off, ACCENT)
    exR, exL = p.pair("exocanthion"); enR, enL = p.pair("endocanthion")
    for q in [exR, enR, enL, exL]:
        _line(guides, (q[0], y0 - fh * 0.3), (q[0], y1), off, INK)
    save("guides", guides)

    # zonas
    eyes_pts = np.vstack([xy[[33, 133, 159, 145, 263, 362, 386, 374]], xy[[70, 105, 107, 300, 334, 336]]])
    ex0, ey0, ex1, ey1 = _bbox(eyes_pts)
    eyes, eoff = _crop(img, ex0, ey0, ex1, ey1, pad=0.25)
    eyes_annot = eyes.copy()
    _draw_points(eyes_annot, np.array([exR[:2], enR[:2], enL[:2], exL[:2]]), eoff, ACCENT)
    for ex, en in [(exR, enR), (exL, enL)]:
        _line(eyes_annot, ex, en, eoff, ACCENT)
    save("eyes", eyes); save("eyes_annot", eyes_annot)

    nose_pts = xy[[168, 6, 1, 2, 129, 358, 49, 279, 9]]
    nx0, ny0, nx1, ny1 = _bbox(nose_pts)
    nose, noff = _crop(img, nx0, ny0, nx1, ny1, pad=0.45, square=True)
    nose_annot = nose.copy(); alR, alL = p.alare()
    _line(nose_annot, alR, alL, noff, ACCENT); _line(nose_annot, p.mid("nasion"), p.mid("subnasale"), noff, INK)
    _draw_points(nose_annot, np.array([alR[:2], alL[:2], p.mid("nasion")[:2], p.mid("subnasale")[:2], p.mid("pronasale")[:2]]), noff, ACCENT)
    save("nose", nose); save("nose_annot", nose_annot)

    mouth_pts = xy[[61, 291, 0, 17, 13, 14, 37, 267, 2, 18]]
    mx0, my0, mx1, my1 = _bbox(mouth_pts)
    mouth, moff = _crop(img, mx0, my0, mx1, my1, pad=0.4)
    mouth_annot = mouth.copy(); chR, chL = p.pair("cheilion")
    _line(mouth_annot, chR, chL, moff, ACCENT); _line(mouth_annot, p.mid("subnasale"), p.mid("labiale_superius"), moff, INK)
    _draw_points(mouth_annot, np.array([chR[:2], chL[:2], p.mid("labiale_superius")[:2], p.mid("labiale_inferius")[:2], p.mid("stomion_sup")[:2]]), moff, ACCENT)
    save("mouth", mouth); save("mouth_annot", mouth_annot)

    low_pts = xy[FACE_OVAL]; low_pts = low_pts[low_pts[:, 1] > p.mid("subnasale")[1] - fh * 0.15]
    lx0, ly0, lx1, ly1 = _bbox(low_pts)
    lower, loff = _crop(img, lx0, ly0, lx1, ly1, pad=0.15)
    lower_annot = lower.copy(); goR, goL = p.pair("gonion"); zyR, zyL = p.pair("zygion")
    _line(lower_annot, goR, goL, loff, ACCENT); _line(lower_annot, zyR, zyL, loff, INK)
    _line(lower_annot, p.mid("sublabiale"), p.mid("menton"), loff, ACCENT)
    _draw_points(lower_annot, np.array([goR[:2], goL[:2], p.mid("menton")[:2], p.mid("pogonion")[:2]]), loff, ACCENT)
    save("lower", lower); save("lower_annot", lower_annot)

    # espejos de simetría: mitad derecha duplicada / mitad izquierda duplicada
    fx = face; fw = fx.shape[1]
    puR, puL = p.pair("pupil"); mid = int((puR[0] + puL[0]) / 2 - off[0])
    mid = max(1, min(fw - 1, mid))
    left_half = fx[:, :mid]; right_half = fx[:, mid:]
    mirror_left = np.hstack([left_half, cv2.flip(left_half, 1)])
    mirror_right = np.hstack([cv2.flip(right_half, 1), right_half])
    save("mirror_left", mirror_left); save("mirror_right", mirror_right)
    return out
