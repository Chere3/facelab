# Estructura del informe (`out/mine/<stem>.json`)

Un informe es un único JSON que crece paso a paso. Las claves principales, en el orden en que aparecen:

```jsonc
{
  "source": "samples/mine/foto_1788665699.jpg",
  "profile": {"sex": "male", "ancestry": "hispanic", "age": 25, "ambition": null},
  "person": "Diego", "date": "2026-09-05 21:34", "feed": true,
  "quality": {"yaw_deg": 1.2, "pitch_deg": -3.4, "roll_deg": 0.8, "blur_laplacian_var": 33.1},
  "warnings": ["imagen borrosa (var. laplaciano 33 < 60)"],

  "measures": {                       // 32 medidas del catálogo
    "facial_index": {"value": 85.1, "unit": "index"},
    "facial_thirds": {"value": {"upper_proxy": 0.18, "middle": 0.42, "lower": 0.40}, "unit": "fraction", "true": {...}},
    "sagittal_angles": {"value": {...}, "unit": "deg", "caveat": "estimado desde la z de la malla"}
  },
  "norms": {                          // percentiles dentro del grupo
    "group": "male|hispanic", "n": 214,
    "per_measure": {"facial_index": {"percentile": 48.1, "mean": 86.0, "z": -0.1}, "facial_thirds.lower": {...}}
  },
  "scores": {
    "symmetry": {"score": 87.4, "percentile": 91.4, "group_mean": 82.0},
    "averageness": {"score": 90.9, "percentile": 71.0},
    "dimorphism": {"masculinity_index": 66.2, "percentile_within_sex": 37.0},
    "proportionality": {"score": 93.2, "percentile": 80.0},
    "global": {"composite": {"score": 70.6, "components": {...}, "weights": {...}},
               "model": {"predicted_rating": 5.82, "percentile_in_group": 37, "r2_cv": 0.36}}
  },

  "assets": {"face": "..._face.jpg", "mesh": "...", "eyes_annot": "...", "mirror_left": "...", "parsing": "..."},
  "age": {"visual_age": 33, "note": "InsightFace buffalo_l; error típico ±6–8 años"},
  "skin": {"redness_pct": 4.1, "spots_pct": 2.3, "texture_index": 3.2, "shine_pct": 1.1, "tone_unevenness": 4.8,
           "maps": {"redness": "..._skin_redness.jpg", ...}, "percentiles": {...}},
  "parsing": {"trichion_y": 412, "hair_visible": true, "glasses": false, "hat": false, "ear_visible": {...}, "facial_thirds_true": {...}},

  "style": {                          // colorimetría y estilo
    "colors": {"skin": {"hex": "#af8d7a", "L": 61.2, "a": 10, "b": 15, "chroma": 18, "hue": 56.3, "depth": "media-clara", "undertone": "neutro"},
               "hair": {"hex": "#323c43", "L": 24.7, "label": "castaño oscuro"}, "eyes": {"hex": "#262a2f", "label": "marrón muy oscuro"}},
    "axes": {"undertone": 0.22, "depth": -0.91, "chroma": -0.18, "contrast_dL": 44.3},
    "contrast": {"level": "medio", "rule": "..."}, "chroma": "medio",
    "season": {"id": "otono_profundo", "name": "Otoño profundo", "secondary": "Invierno profundo", "margin": 1.14, "ranking": [...], "summary": "...", "why": [...]},
    "palette": {"best": [{"hex": "#4a0e0e", "name": "granate"}, ...], "neutrals": [...], "avoid": [...], "metals": "oro amarillo, bronce, cobre", "hair_colors": [...], "makeup": [...], "patterns": "..."},
    "face_shape": {"id": "oval", "name": "Ovalada", "scores": {...}, "inputs": {...}},
    "hair": {"visible": true, "length": "medio", "width_to_face": 1.44},
    "bust": "..._bust.jpg",
    "shirts": {"mode": "recolor", "cloth_fraction": 0.095, "items": [{"hex": "#4a0e0e", "name": "granate", "group": "best", "file": "..._shirt_00.jpg"}, ...]},
    "advice": {"summary": "...", "color_story": "...", "wardrobe": [...], "outfits": [{"id": "casual", "name": "...", "expression": "neutral", "pieces": [...], "colors": [...], "accessories": [...], "grooming": "...", "why": "...", "render_prompt": "..."}],
               "haircuts": [...], "grooming": [...], "hair_color": [...], "avoid": [...]},
    "renders": {"casual": {"file": "..._look_casual.jpg", "png": "..._look_casual.png", "kind": "outfit", "prompt": "...", "ts": 1788669046}}
  },

  "profile_view": {"facing": "right", "points": {...}, "measures": {"nasofrontal": {"value": 138.6, "range": "115–135°", "source": "Powell & Humphreys"}, ...}, "image": "..._profile.jpg"},

  "narrative": {"proporciones": {"summary": "...", "findings": [{"measure": "facial_index", "statement": "..."}], "strengths": [...], "watch": [...]}, "ojos_y_cejas": {...}, ...},
  "protocol": {"intensity": {"tier": "mejora", "computed": "mejora", "requested": null, "drivers": [...], "rationale": "..."},
               "target_look": "...", "phases": [{"name": "...", "weeks": "0–4 semanas", "goal": "...", "actions": [{"method_id": "retinoid_night", "name": "...", "why": "...", "spec": "...", "cost": "...", "frequency": "...", "horizon": "...", "difficulty": "...", "evidence": "A"}]}],
               "expected_changes": [{"measure": "...", "now": "...", "target": "...", "via": "..."}], "not_recommended": [...], "letter": "..."},
  "visualization": {"model": "gpt-5.5", "tier": "mejora", "edits": [...], "after": "..._after.png", "after_3m": "..._after_3m.png", "prompt": "..."},
  "review": {"approved": true, "by": "Ana", "notes": "..."}
}
```

## Reglas

- **Unidades**: `ratio`, `deg`, `index`, `fraction`, `px`. Las de `px` no tienen percentil.
- **`caveat`** en una medida significa orientativa. La narrativa está obligada a decirlo.
- **Percentil**: 40–60 típico; 25–40 y 60–75 ligeramente por debajo o encima; <25 y >75 claramente. No hay más rangos.
- **Regeneración**: cada paso escribe solo su clave y conserva la anterior si falla (`narrative`, `protocol`, `style.advice`).
- **Escritura atómica**: `.json.tmp` → `rename`. Si un lector ve `409 escribiendo`, reintenta.
