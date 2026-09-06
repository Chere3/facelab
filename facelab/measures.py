"""Cálculo de las medidas del catálogo a partir de los 478 puntos."""
from __future__ import annotations
from pathlib import Path
import math
import numpy as np
import yaml
from .points import P
from .geometry import dist, angle_deg_3d, align_roll, symmetry, midline_x

CATALOG = yaml.safe_load((Path(__file__).parent / "catalog.yaml").read_text())
CATALOG_BY_ID = {c["id"]: c for c in CATALOG}


def _r(x, n=3):
    return None if x is None else round(float(x), n)


def compute(pts_raw: np.ndarray) -> dict:
    pts, roll = align_roll(pts_raw)
    p = P(pts)
    m: dict[str, dict] = {}

    def put(mid, value, **extra):
        entry = {"value": value, "unit": CATALOG_BY_ID[mid]["unit"]}
        entry.update(extra)
        m[mid] = entry

    # --- puntos base
    fh, gl, na, prn, sn = p.mid("forehead_top"), p.mid("glabella"), p.mid("nasion"), p.mid("pronasale"), p.mid("subnasale")
    ls, sto_s, sto_i, li, sl, pg, me = (p.mid(k) for k in ["labiale_superius", "stomion_sup", "stomion_inf", "labiale_inferius", "sublabiale", "pogonion", "menton"])
    exR, exL = p.pair("exocanthion"); enR, enL = p.pair("endocanthion")
    esR, esL = p.pair("eyelid_sup"); eiR, eiL = p.pair("eyelid_inf")
    puR, puL = p.pair("pupil"); zyR, zyL = p.pair("zygion"); goR, goL = p.pair("gonion")
    chR, chL = p.pair("cheilion"); clR, clL = p.pair("chin_lat")
    alR, alL = p.alare()
    bhR, bhL = p.pair("brow_head"); baR, baL = p.pair("brow_apex"); btR, btL = p.pair("brow_tail")

    face_h = dist(na, me)
    bizy = dist(zyR, zyL)
    oval = p.oval()
    eye_y = (puR[1] + puL[1]) / 2
    # borde del óvalo a la altura de los ojos (interpolación por fila más cercana)
    ov_right = oval[oval[:, 0] < midline_x(pts)]
    ov_left = oval[oval[:, 0] > midline_x(pts)]
    edge_r = ov_right[np.argmin(np.abs(ov_right[:, 1] - eye_y))]
    edge_l = ov_left[np.argmin(np.abs(ov_left[:, 1] - eye_y))]

    # --- tercios
    upper = dist(fh, gl); middle = dist(gl, sn); lower = dist(sn, me)
    tot = upper + middle + lower
    put("facial_thirds", {"upper_proxy": _r(upper / tot), "middle": _r(middle / tot), "lower": _r(lower / tot)},
        middle_to_lower=_r(middle / lower), caveat=CATALOG_BY_ID["facial_thirds"]["note"])

    # --- quintos
    segs = [dist(edge_r, exR), dist(exR, enR), dist(enR, enL), dist(enL, exL), dist(exL, edge_l)]
    tw = sum(segs)
    put("facial_fifths", {"outer_R": _r(segs[0] / tw), "eye_R": _r(segs[1] / tw), "intercanthal": _r(segs[2] / tw),
                          "eye_L": _r(segs[3] / tw), "outer_L": _r(segs[4] / tw)})

    put("facial_index", _r(face_h / bizy * 100, 1))
    upper_face = dist((esR + esL) / 2, ls)
    put("fwhr", _r(bizy / upper_face))

    icw = dist(enR, enL); ipd = dist(puR, puL)
    put("intercanthal_width", _r(icw, 1)); put("interpupillary_distance", _r(ipd, 1)); put("biocular_width", _r(dist(exR, exL), 1))
    ewR, ewL = dist(exR, enR), dist(exL, enL)
    ehR, ehL = dist(esR, eiR), dist(esL, eiL)
    put("eye_width", {"R": _r(ewR, 1), "L": _r(ewL, 1)})
    put("eye_height", {"R": _r(ehR, 1), "L": _r(ehL, 1)})
    put("eye_aspect_ratio", {"R": _r(ehR / ewR), "L": _r(ehL / ewL)})

    def tilt(ex, en):
        # + si el canto externo está más alto (y menor en imagen)
        return math.degrees(math.atan2(en[1] - ex[1], abs(ex[0] - en[0])))
    put("canthal_tilt", {"R": _r(tilt(exR, enR), 1), "L": _r(tilt(exL, enL), 1)})
    put("eye_spacing_ratio", _r(icw / ((ewR + ewL) / 2)))

    nw = dist(alR, alL); nh = dist(na, sn)
    put("nose_width", _r(nw, 1)); put("nasal_height", _r(nh, 1)); put("nasal_index", _r(nw / nh * 100, 1))
    put("nose_to_intercanthal", _r(nw / icw))

    mw = dist(chR, chL)
    put("mouth_width", _r(mw, 1)); put("mouth_to_nose", _r(mw / nw))
    put("philtrum_length", _r(dist(sn, ls), 1))
    ul, ll = dist(ls, sto_s), dist(sto_i, li)
    put("lip_ratio", _r(ul / ll if ll > 0 else None), upper_px=_r(ul, 1), lower_px=_r(ll, 1))
    put("lip_height_to_mouth_width", _r((ul + ll) / mw))
    sto = (sto_s + sto_i) / 2
    ctR = math.degrees(math.atan2(sto[1] - chR[1], abs(chR[0] - sto[0])))
    ctL = math.degrees(math.atan2(sto[1] - chL[1], abs(chL[0] - sto[0])))
    put("commissure_tilt", _r((ctR + ctL) / 2, 1), R=_r(ctR, 1), L=_r(ctL, 1))

    put("lower_face_height", _r(lower, 1)); chin_h = dist(sl, me)
    put("chin_height", _r(chin_h, 1)); put("chin_to_lower_face", _r(chin_h / lower))

    bigo = dist(goR, goL)
    put("bigonial_width", _r(bigo, 1)); put("bizygomatic_width", _r(bizy, 1)); put("jaw_to_cheek", _r(bigo / bizy))
    put("chin_width_to_jaw", _r(dist(clR, clL) / bigo))

    bpR = (puR[1] - baR[1]) / ewR; bpL = (puL[1] - baL[1]) / ewL
    put("brow_position", {"R": _r(bpR), "L": _r(bpL)})
    btilt = lambda h, t: math.degrees(math.atan2(h[1] - t[1], abs(t[0] - h[0])))
    put("brow_tilt", {"R": _r(btilt(bhR, btR), 1), "L": _r(btilt(bhL, btL), 1)})

    pu_mid = (puR + puL) / 2
    put("midface_ratio", _r(ipd / dist(pu_mid, ls)))

    put("symmetry", symmetry(pts, face_h)["score"], detail=symmetry(pts, face_h))

    # --- sagitales estimados (plano y-z): usar z de MediaPipe
    put("sagittal_angles", {
        "nasofrontal": _r(angle_deg_3d(gl, na, prn, axes=(1, 2)), 1),
        "nasolabial": _r(angle_deg_3d(prn, sn, ls, axes=(1, 2)), 1),
        "mentolabial": _r(angle_deg_3d(li, sl, pg, axes=(1, 2)), 1),
    }, caveat=CATALOG_BY_ID["sagittal_angles"]["note"])

    return {"roll_corrected_deg": _r(roll, 2), "face_height_px": _r(face_h, 1), "measures": m}
