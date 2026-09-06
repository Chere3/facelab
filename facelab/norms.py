"""Normas empíricas: percentiles por grupo demográfico y scores globales a partir de MEBeauty.

Grupos: "<sex>|<ancestry>", con caída a "<sex>|all" si el grupo es pequeño y a "all|all" si no hay sexo.
"""
from __future__ import annotations
import json
from functools import lru_cache
from pathlib import Path
import numpy as np
from .measures import CATALOG_BY_ID

FEATURES = Path(__file__).resolve().parent.parent / "norms" / "mebeauty_features.jsonl"
ANCESTRIES = ["asian", "black", "caucasian", "hispanic", "indian", "mideastern"]
MIN_GROUP = 40
# medidas escalares que entran en el score de proporcionalidad (ratios e índices, sin px)
PROPORTION_KEYS = ["facial_thirds.middle", "facial_thirds.lower", "facial_fifths.eye_R", "facial_fifths.eye_L",
                   "facial_fifths.intercanthal", "facial_index", "fwhr", "eye_spacing_ratio", "nasal_index",
                   "nose_to_intercanthal", "mouth_to_nose", "lip_ratio", "chin_to_lower_face", "jaw_to_cheek",
                   "midface_ratio", "eye_aspect_ratio.R", "eye_aspect_ratio.L"]


def comparable(key: str) -> bool:
    """Solo ratios, índices, fracciones, ángulos y scores se comparan entre fotos; los px dependen de la escala."""
    return CATALOG_BY_ID.get(key.split(".")[0], {}).get("unit") not in (None, "px")


class Norms:
    def __init__(self, path: Path = FEATURES):
        self.rows = [json.loads(l) for l in open(path)] if path.exists() else []
        self.shapes = np.array([r["shape"] for r in self.rows]) if self.rows else None

    # ---- grupos
    def idx(self, sex: str | None, ancestry: str | None) -> tuple[np.ndarray, str]:
        def sel(s, a):
            return np.array([i for i, r in enumerate(self.rows) if (s in (None, "all") or r["sex"] == s) and (a in (None, "all") or r["ancestry"] == a)])
        for s, a in [(sex, ancestry), (sex, "all"), ("all", "all")]:
            ix = sel(s, a)
            if len(ix) >= MIN_GROUP:
                return ix, f"{s or 'all'}|{a or 'all'}"
        return np.arange(len(self.rows)), "all|all"

    def values(self, key: str, ix: np.ndarray) -> np.ndarray:
        v = [self.rows[i]["measures"].get(key) for i in ix]
        return np.array([x for x in v if x is not None], dtype=float)

    @staticmethod
    def percentile_of(x: float, arr: np.ndarray) -> float | None:
        if arr.size == 0:
            return None
        return float(np.round((arr < x).mean() * 100 + (arr == x).mean() * 50, 1))

    # ---- enriquecer medidas con percentil y z del grupo
    def enrich(self, flat_measures: dict[str, float], sex: str | None, ancestry: str | None) -> dict:
        ix, group = self.idx(sex, ancestry)
        out = {}
        for k, x in flat_measures.items():
            if x is None or k in ("symmetry",) or not comparable(k):
                continue
            arr = self.values(k, ix)
            if arr.size < MIN_GROUP:
                continue
            mean, sd = float(arr.mean()), float(arr.std())
            out[k] = {"percentile": self.percentile_of(x, arr), "group_mean": round(mean, 3), "group_sd": round(sd, 3),
                      "z": round((x - mean) / sd, 2) if sd > 0 else None}
        return {"group": group, "n": int(len(ix)), "per_measure": out}

    # ---- scores globales
    def averageness(self, shape: np.ndarray, sex, ancestry) -> dict:
        ix, group = self.idx(sex, ancestry)
        S = self.shapes[ix]
        mean_shape = S.mean(axis=0)
        d_all = np.linalg.norm((S - mean_shape).reshape(len(S), -1), axis=1)
        d = float(np.linalg.norm((shape - mean_shape).ravel()))
        pct = self.percentile_of(d, d_all)  # % del grupo más cerca de la media que tú
        return {"score": round(100 - pct, 1), "distance": round(d, 4), "group": group, "n": int(len(ix)),
                "note": "100 = la cara más próxima a la media de su grupo; 0 = la más alejada"}

    def dimorphism(self, shape: np.ndarray, sex, ancestry) -> dict:
        ixm, gm = self.idx("male", ancestry); ixf, gf = self.idx("female", ancestry)
        if gm.split("|")[1] != gf.split("|")[1]:
            ixm, _ = self.idx("male", "all"); ixf, _ = self.idx("female", "all")
        M, F = self.shapes[ixm].reshape(len(ixm), -1), self.shapes[ixf].reshape(len(ixf), -1)
        axis = M.mean(0) - F.mean(0); axis /= np.linalg.norm(axis) + 1e-9
        pm, pf = M @ axis, F @ axis
        p = float(shape.ravel() @ axis)
        # índice = percentil sobre hombres y mujeres del grupo juntos: 0 = forma más femenina, 100 = más masculina
        pooled = np.concatenate([pm, pf])
        own = pm if sex == "male" else pf
        return {"masculinity_index": self.percentile_of(p, pooled),
                "percentile_within_sex": self.percentile_of(p, own) if sex in ("male", "female") else None,
                "raw_position": round(float((p - pf.mean()) / (pm.mean() - pf.mean() + 1e-9) * 100), 1),
                "group_ancestry": gm.split("|")[1], "n_male": int(len(ixm)), "n_female": int(len(ixf)),
                "note": "percentil de masculinidad de forma entre hombres y mujeres de tu ascendencia (0 = más femenina, 100 = más masculina); percentil dentro de tu sexo aparte"}

    def proportionality(self, flat_measures: dict, sex, ancestry) -> dict:
        ix, group = self.idx(sex, ancestry)
        keys = [k for k in PROPORTION_KEYS if flat_measures.get(k) is not None]
        stats = {k: (self.values(k, ix).mean(), self.values(k, ix).std()) for k in keys}
        def mean_abs_z(m):
            zs = [abs((m[k] - stats[k][0]) / stats[k][1]) for k in keys if m.get(k) is not None and stats[k][1] > 0]
            return float(np.mean(zs)) if zs else None
        user = mean_abs_z(flat_measures)
        grp = np.array([v for v in (mean_abs_z(self.rows[i]["measures"]) for i in ix) if v is not None])
        pct = self.percentile_of(user, grp)
        return {"score": round(100 - pct, 1), "mean_abs_z": round(user, 3), "group": group, "n": int(len(ix)),
                "note": "100 = proporciones más cercanas a la media del grupo en 17 ratios; 0 = más alejadas"}

    def symmetry_percentile(self, score: float, sex, ancestry) -> dict:
        ix, group = self.idx(sex, ancestry)
        arr = self.values("symmetry", ix)
        return {"percentile": self.percentile_of(score, arr), "group": group, "group_mean": round(float(arr.mean()), 1) if arr.size else None}

    def skin_percentiles(self, skin: dict, sex, ancestry) -> dict:
        path = FEATURES.parent / "mebeauty_skin.jsonl"
        if not path.exists():
            return {}
        rows = [json.loads(l) for l in open(path)]
        def sel(s, a):
            return [r for r in rows if (s in (None, "all") or r["sex"] == s) and (a in (None, "all") or r["ancestry"] == a)]
        grp, name = None, "all|all"
        for s, a in [(sex, ancestry), (sex, "all"), ("all", "all")]:
            g = sel(s, a)
            if len(g) >= MIN_GROUP:
                grp, name = g, f"{s or 'all'}|{a or 'all'}"; break
        grp = grp or rows
        out = {"group": name, "n": len(grp)}
        for k in ("redness_pct", "spots_pct", "texture_index", "shine_pct", "tone_unevenness"):
            arr = np.array([r["skin"][k] for r in grp if k in r["skin"]], dtype=float); arr = arr[~np.isnan(arr)]
            if arr.size >= MIN_GROUP and skin.get(k) is not None and not np.isnan(skin[k]):
                out[k] = {"percentile": self.percentile_of(skin[k], arr), "group_mean": round(float(arr.mean()), 3)}
        return out

    def attractiveness_correlations(self, sex, ancestry, top=12) -> list[dict]:
        """Qué medidas correlacionan con la puntuación humana en este dataset (informativo, no causal)."""
        ix, group = self.idx(sex, ancestry)
        rows = [self.rows[i] for i in ix if self.rows[i].get("score") is not None]
        if len(rows) < MIN_GROUP:
            return []
        y = np.array([r["score"] for r in rows])
        out = []
        for k in rows[0]["measures"]:
            if not comparable(k):
                continue
            x = np.array([r["measures"].get(k) if r["measures"].get(k) is not None else np.nan for r in rows], dtype=float)
            ok = ~np.isnan(x)
            if ok.sum() < MIN_GROUP or x[ok].std() == 0:
                continue
            r = float(np.corrcoef(x[ok], y[ok])[0, 1])
            out.append({"measure": k, "r": round(r, 3), "n": int(ok.sum())})
        out.sort(key=lambda d: -abs(d["r"]))
        return out[:top]


@lru_cache(maxsize=1)
def get_norms() -> Norms:
    return Norms()
