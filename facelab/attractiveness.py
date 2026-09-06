"""Puntuación global de atractivo.

Dos lecturas complementarias:
1. `composite`: combinación ponderada de los marcos ya medidos (averageness, dimorfismo alineado con el sexo, piel, simetría,
   proporcionalidad, perfil, edad visual), cada uno en 0–100. Pesos orientados por la literatura (Rhodes 2006; Fink et al. 2001;
   Jones et al. 2004; Foo et al. 2017): averageness y dimorfismo pesan más que simetría.
2. `model`: regresión ridge entrenada con las valoraciones humanas de MEBeauty (1–10, ~300 evaluadores) sobre las mismas
   medidas, forma (PCA) y piel. Devuelve la valoración prevista, su percentil dentro del grupo y la fiabilidad del modelo (R², r en CV).
"""
from __future__ import annotations
import json
from functools import lru_cache
from pathlib import Path
import numpy as np
from .norms import comparable, get_norms, ANCESTRIES, MIN_GROUP

NORMS_DIR = Path(__file__).resolve().parent.parent / "norms"
MODEL_PATH = NORMS_DIR / "attractiveness_model.json"
SKIN_KEYS = ["redness_pct", "spots_pct", "texture_index", "shine_pct", "tone_unevenness"]
N_PCA = 25
WEIGHTS = {"averageness": 0.25, "dimorphism": 0.20, "skin": 0.20, "symmetry": 0.10, "proportionality": 0.10, "profile": 0.10, "visual_age": 0.05}


# ------------------------------------------------------------------ datos
def _load_rows():
    rows = [json.loads(l) for l in open(NORMS_DIR / "mebeauty_features.jsonl")]
    skin = {}
    p = NORMS_DIR / "mebeauty_skin.jsonl"
    if p.exists():
        skin = {json.loads(l)["file"]: json.loads(l)["skin"] for l in open(p)}
    for r in rows:
        r["skin"] = skin.get(r["file"], {})
    return rows


def _measure_keys(rows):
    keys = sorted({k for r in rows for k in r["measures"] if comparable(k) and k != "symmetry"})
    return keys + ["symmetry"]


def _vec(measures: dict, skin: dict, shape_pc: np.ndarray, sex: str | None, ancestry: str | None, keys: list[str]) -> np.ndarray:
    m = [measures.get(k) if measures.get(k) is not None else np.nan for k in keys]
    s = [skin.get(k) if skin.get(k) is not None else np.nan for k in SKIN_KEYS]
    sx = [1.0 if sex == "male" else 0.0, 1.0 if sex == "female" else 0.0]
    # la ascendencia NO entra como feature: codificaría el sesgo de los evaluadores; los percentiles ya se calculan por grupo
    return np.array(m + s + sx + list(shape_pc), dtype=float)


# ------------------------------------------------------------------ entrenamiento
def train(verbose: bool = True) -> dict:
    rows = [r for r in _load_rows() if r.get("score") is not None]
    keys = _measure_keys(rows)
    shapes = np.array([np.ravel(r["shape"]) for r in rows])
    mean_shape = shapes.mean(0)
    U, S, Vt = np.linalg.svd(shapes - mean_shape, full_matrices=False)
    comps = Vt[:N_PCA]
    X = np.array([_vec(r["measures"], r["skin"], (np.ravel(r["shape"]) - mean_shape) @ comps.T, r["sex"], r["ancestry"], keys) for r in rows])
    y = np.array([r["score"] for r in rows])
    col_mean = np.nanmean(X, 0); X = np.where(np.isnan(X), col_mean, X)
    mu, sd = X.mean(0), X.std(0) + 1e-9
    Xs = (X - mu) / sd
    # CV 5-fold para elegir lambda
    rng = np.random.default_rng(0); idx = rng.permutation(len(y)); folds = np.array_split(idx, 5)
    best = None
    for lam in [1, 3, 10, 30, 100, 300]:
        preds = np.zeros(len(y))
        for f in folds:
            tr = np.setdiff1d(idx, f)
            w, b = _ridge(Xs[tr], y[tr], lam)
            preds[f] = Xs[f] @ w + b
        r = float(np.corrcoef(preds, y)[0, 1]); r2 = 1 - float(((y - preds) ** 2).sum() / ((y - y.mean()) ** 2).sum())
        if best is None or r2 > best[1]:
            best = (lam, r2, r, preds.copy())
    lam, r2, r, cv_preds = best
    w, b = _ridge(Xs, y, lam)
    fitted = Xs @ w + b
    model = {"keys": keys, "skin_keys": SKIN_KEYS, "ancestries": ANCESTRIES, "n_pca": N_PCA, "mean_shape": mean_shape.tolist(), "components": comps.tolist(),
             "col_mean": col_mean.tolist(), "mu": mu.tolist(), "sd": sd.tolist(), "w": w.tolist(), "b": float(b), "lambda": lam,
             "cv_r2": round(r2, 3), "cv_r": round(r, 3), "n": int(len(y)), "score_mean": round(float(y.mean()), 3), "score_sd": round(float(y.std()), 3),
             "group_preds": [{"sex": rows[i]["sex"], "ancestry": rows[i]["ancestry"], "pred": round(float(fitted[i]), 3), "score": float(y[i])} for i in range(len(rows))],
             "top_features": sorted([(keys + SKIN_KEYS + ["sex_m", "sex_f"] + [f"pc{i}" for i in range(N_PCA)])[i] + f":{w[i]:+.3f}" for i in np.argsort(-np.abs(w))[:15]], key=lambda s: -abs(float(s.split(":")[1])))}
    MODEL_PATH.write_text(json.dumps(model))
    if verbose:
        print(f"n={len(y)} lambda={lam} CV R²={r2:.3f} r={r:.3f}")
        print("features más influyentes (coef estandarizado):", model["top_features"][:10])
    return model


def _ridge(X, y, lam):
    n, d = X.shape
    Xb = np.hstack([X, np.ones((n, 1))])
    reg = lam * np.eye(d + 1); reg[-1, -1] = 0
    wb = np.linalg.solve(Xb.T @ Xb + reg, Xb.T @ y)
    return wb[:-1], wb[-1]


@lru_cache(maxsize=1)
def _model():
    if not MODEL_PATH.exists():
        return None
    return json.loads(MODEL_PATH.read_text())


# ------------------------------------------------------------------ predicción
def model_score(report: dict) -> dict | None:
    M = _model()
    if not M or "shape" not in report:
        return None
    from .repeat import flat
    fm = flat(report["measures"])
    prof = report.get("profile") or {}
    sex, anc = prof.get("sex"), (None if prof.get("ancestry") in (None, "other") else prof.get("ancestry"))
    shape = np.ravel(report["shape"]) - np.array(M["mean_shape"])
    pc = shape @ np.array(M["components"]).T
    x = _vec(fm, report.get("skin") or {}, pc, sex, anc, M["keys"])
    x = np.where(np.isnan(x), np.array(M["col_mean"]), x)
    pred = float(((x - np.array(M["mu"])) / np.array(M["sd"])) @ np.array(M["w"]) + M["b"])
    pred = float(np.clip(pred, 1, 10))
    grp = [g for g in M["group_preds"] if (sex in (None, "all") or g["sex"] == sex) and (anc is None or g["ancestry"] == anc)]
    name = f"{sex or 'all'}|{anc or 'all'}"
    if len(grp) < MIN_GROUP:
        grp = [g for g in M["group_preds"] if sex in (None, "all") or g["sex"] == sex]; name = f"{sex or 'all'}|all"
    preds = np.array([g["pred"] for g in grp]); human = np.array([g["score"] for g in grp])
    pct = get_norms().percentile_of(pred, preds)
    return {"predicted_rating": round(pred, 2), "scale": "1–10 (MEBeauty, ~300 evaluadores)", "percentile_in_group": pct, "group": name, "n_group": int(len(grp)),
            "group_human_mean": round(float(human.mean()), 2), "cv_r2": M["cv_r2"], "cv_r": M["cv_r"], "n_train": M["n"],
            "note": f"El modelo explica el {int(M['cv_r2']*100)} % de la varianza de las valoraciones humanas (r={M['cv_r']}); el resto depende de expresión, estilo, luz y gusto del evaluador."}


# ------------------------------------------------------------------ compuesto por marcos
def composite(report: dict) -> dict:
    s = report.get("scores") or {}
    prof = report.get("profile") or {}
    comp, notes = {}, {}
    if s.get("averageness"):
        comp["averageness"] = s["averageness"]["score"]
    if s.get("dimorphism") and s["dimorphism"].get("masculinity_index") is not None:
        mi = s["dimorphism"]["masculinity_index"]
        comp["dimorphism"] = mi if prof.get("sex") == "male" else (100 - mi if prof.get("sex") == "female" else 50)
        notes["dimorphism"] = "masculinidad de forma si eres hombre, feminidad si eres mujer"
    if s.get("symmetry"):
        comp["symmetry"] = s["symmetry"].get("percentile") if s["symmetry"].get("percentile") is not None else s["symmetry"]["score"]
    if s.get("proportionality"):
        comp["proportionality"] = s["proportionality"]["score"]
    sk = (report.get("skin") or {}).get("percentiles") or {}
    vals = [100 - sk[k]["percentile"] for k in SKIN_KEYS if sk.get(k) and sk[k].get("percentile") is not None]
    if vals:
        comp["skin"] = round(float(np.mean(vals)), 1); notes["skin"] = "100 = menos rojez, manchas, textura, brillo y desigualdad de tono que tu grupo"
    pv = report.get("profile_view")
    if pv and pv.get("measures"):
        ok, tot = 0, 0
        for k, v in pv["measures"].items():
            rng = _parse_range(v.get("range", ""))
            if rng:
                tot += 1; lo, hi = rng; x = v["value"]
                ok += 1 if lo <= x <= hi else max(0.0, 1 - abs(x - (lo if x < lo else hi)) / (hi - lo + 1e-9))
        if tot:
            comp["profile"] = round(ok / tot * 100, 1); notes["profile"] = f"{tot} medidas de perfil dentro o cerca de su norma"
    age = (report.get("age") or {}).get("visual_age"); declared = prof.get("age")
    if age is not None:
        ref = declared if declared else age
        comp["visual_age"] = round(float(np.clip(50 + (ref - age) * 3, 0, 100)), 1)
        notes["visual_age"] = "50 = pareces tu edad; ±3 puntos por cada año de diferencia (el estimador tiene ±6–8 años de error)" if declared else "sin edad declarada: neutro"
    comp = {k: round(float(np.clip(v, 0, 100)), 1) for k, v in comp.items()}
    used = {k: WEIGHTS[k] for k in comp}
    tw = sum(used.values()) or 1
    score = sum(comp[k] * used[k] for k in comp) / tw
    return {"score": round(float(score), 1), "components": comp, "weights": {k: round(v / tw, 3) for k, v in used.items()}, "notes": notes,
            "missing": [k for k in WEIGHTS if k not in comp],
            "method": "media ponderada de marcos (0–100); pesos de Rhodes 2006 (averageness, dimorfismo), Fink 2001 y Jones 2004 (piel), Foo 2017 (simetría débil)"}


def _parse_range(text: str):
    import re
    m = re.findall(r"[−\-]?\d+(?:\.\d+)?", text.replace("–", "-").replace("−", "-"))
    if len(m) >= 2:
        try:
            a, b = float(m[0]), float(m[1]); return (min(a, b), max(a, b))
        except ValueError:
            return None
    return None


def compute(report: dict) -> dict:
    out = {"composite": composite(report)}
    ms = model_score(report)
    if ms:
        out["model"] = ms
    return out


if __name__ == "__main__":
    train()
