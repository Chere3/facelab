"""Protocolo con intensidad proporcional al caso.

1. `assess_intensity`: cuenta desviaciones relevantes (percentiles extremos en dirección desfavorable, piel, edad visual, scores
   globales) y clasifica en `mantenimiento`, `mejora` o `glow-up`.
2. Claude diseña el plan con la biblioteca (`methods.yaml`), respetando el nivel: en glow-up se exige un plan de 12 meses con
   cambios de peso real (pelo, barba, cuerpo con cifras, dientes, piel profesional, cejas, gafas, estilo) y un "look objetivo"
   descrito con precisión, que después alimenta las imágenes de Codex.
Salida: {"intensity", "target_look", "phases", "expected_changes", "not_recommended", "letter"}
"""
from __future__ import annotations
import json, re
from pathlib import Path
import anyio, yaml
from claude_agent_sdk import query, ClaudeAgentOptions, AssistantMessage, TextBlock

METHODS = yaml.safe_load((Path(__file__).parent / "methods.yaml").read_text())
MODEL = "claude-sonnet-5"

# medidas donde un percentil BAJO es desfavorable / ALTO es desfavorable (dirección estética habitual, orientativa)
LOW_BAD = ["eye_aspect_ratio", "brow_position", "canthal_tilt", "jaw_to_cheek", "lip_ratio", "mouth_to_nose", "chin_to_lower_face", "facial_thirds.middle"]
HIGH_BAD = ["facial_index", "nose_to_intercanthal", "nasal_index", "eye_spacing_ratio", "philtrum_length", "facial_thirds.lower"]
SKIN_KEYS = ["redness_pct", "spots_pct", "texture_index", "shine_pct", "tone_unevenness"]


def _pct(report, key):
    pm = (report.get("norms") or {}).get("per_measure") or {}
    if key in pm:
        return pm[key].get("percentile")
    vals = [v.get("percentile") for k, v in pm.items() if k.startswith(key + ".") and v.get("percentile") is not None]
    return sum(vals) / len(vals) if vals else None


def assess_intensity(report: dict) -> dict:
    drivers, score = [], 0.0
    for k in LOW_BAD:
        p = _pct(report, k)
        if p is not None and p < 15: drivers.append(f"{k} p{p:.0f} (bajo)"); score += 1.5 if p < 8 else 1
    for k in HIGH_BAD:
        p = _pct(report, k)
        if p is not None and p > 85: drivers.append(f"{k} p{p:.0f} (alto)"); score += 1.5 if p > 92 else 1
    sk = (report.get("skin") or {}).get("percentiles") or {}
    for k in SKIN_KEYS:
        p = (sk.get(k) or {}).get("percentile")
        if p is not None and p > 70: drivers.append(f"piel {k} p{p:.0f}"); score += 1 if p < 85 else 1.5
    age = (report.get("age") or {}).get("visual_age"); declared = (report.get("profile") or {}).get("age")
    if age and declared and age >= declared + 5: drivers.append(f"edad visual {age} vs {declared} declarada"); score += 1.5
    g = ((report.get("scores") or {}).get("global") or {})
    comp = (g.get("composite") or {}).get("score"); mp = (g.get("model") or {}).get("percentile_in_group")
    if comp is not None and comp < 45: drivers.append(f"compuesto global {comp}"); score += 1.5
    if mp is not None and mp < 30: drivers.append(f"valoración prevista p{mp:.0f}"); score += 1.5
    s = report.get("scores") or {}
    if s.get("proportionality") and s["proportionality"]["score"] < 20: drivers.append("proporcionalidad muy baja"); score += 1
    if s.get("symmetry") and (s["symmetry"].get("percentile") or 50) < 15: drivers.append("asimetría marcada"); score += 0.5
    computed = "glow-up" if score >= 5 else ("mejora" if score >= 2 else "mantenimiento")
    order = ["mantenimiento", "mejora", "glow-up"]
    wanted = (report.get("profile") or {}).get("ambition")
    tier = computed
    if wanted in order and order.index(wanted) > order.index(computed):
        tier = wanted; drivers.append(f"nivel pedido por el usuario: {wanted}")
    return {"tier": tier, "computed": computed, "requested": wanted, "score": round(score, 1), "drivers": drivers,
            "rationale": {"glow-up": "varias desviaciones relevantes a la vez: el caso amerita un plan de 12 meses con cambios de peso real",
                          "mejora": "algunas desviaciones claras: plan de 6 meses centrado en ellas",
                          "mantenimiento": "pocas desviaciones: hábitos, piel y encuadre; nada que forzar"}[tier]}


SYSTEM = """Eres el director de protocolos de un servicio de transformación estética no quirúrgica (estilo glow-up). Escribes en español, directo y concreto.
Recibes: perfil, medidas con percentiles, scores globales, narrativa, edad visual, piel, un NIVEL DE INTENSIDAD calculado y una BIBLIOTECA de métodos (con tier: basic, intensive, professional).
Reglas:
- Solo recomiendas métodos de la biblioteca, citando method_id. Puedes concretar cada uno (qué corte exacto, qué color, cuántos kg, qué zona) en "why" y "spec".
- El plan DEBE respetar el nivel:
  · mantenimiento: 4–6 acciones, 2 fases (0–1 y 1–3 meses), solo tier basic.
  · mejora: 7–10 acciones, 3 fases (0–1, 1–3, 3–6 meses), basic + intensive.
  · glow-up: 11–16 acciones, 4 fases (0–1, 1–3, 3–6, 6–12 meses). Obligatorio incluir, si el sexo y los hallazgos lo permiten: transformación de pelo con corte descrito (largo, laterales, volumen, textura) y color si mejora el contraste; barba (hombres) o cejas rediseñadas (todos); recomposición corporal con objetivo numérico si hay adiposidad facial o mandíbula poco definida; plan dental; programa de piel profesional si la piel está en percentil >60; gafas/lentillas y paleta de ropa; postura y sueño. Los métodos tier professional (botox, relleno) solo si un percentil es extremo (<10 o >90) en la zona que tratan, siempre con médico y dicho explícitamente.
- Cada acción explica en 1–2 frases por qué aplica A ESTA persona, citando medida y percentil, y "spec" con el detalle ejecutable (p. ej. "corte: 8–10 cm arriba con volumen, laterales a 3 mm, raya lateral; color: castaño oscuro frío").
- "target_look": un párrafo de 5–8 frases que describa con precisión visual cómo se verá la persona al final (pelo, barba/cejas, piel, cara más o menos definida, dientes, gafas, ropa), citando qué NO cambia (rasgos óseos, ojos, nariz). Es la guía para generar la imagen; sé específico y realista.
- "expected_changes": 5–10 filas {measure, now, target, via} con la medida (id), su percentil actual, el objetivo realista y qué método lo mueve. Para lo que no cambia sin cirugía (nariz, hueso), dilo en not_recommended.
- Si recibes "style" (colorimetría medida), las acciones de ropa, gafas, corte y color de pelo deben ser coherentes con su estación, paleta, contraste y forma de cara; cita la estación en el spec.
- Lo que ya está en rango típico NO se toca: not_recommended. La asimetría leve es normal. Nada de cirugía.
- "letter": 5–7 frases, tono de entrenador exigente pero honesto, sin adulación, sin prometer.
- Devuelve SOLO JSON: {"target_look":"","phases":[{"name":"","weeks":"","goal":"","actions":[{"method_id":"","name":"","why":"","spec":"","cost":"","frequency":"","horizon":"","difficulty":"","evidence":""}]}],"expected_changes":[{"measure":"","now":"","target":"","via":""}],"not_recommended":[""],"letter":""}"""


def extract_json(text: str):
    t = re.sub(r"^\s*```(?:json)?\s*|\s*```\s*$", "", text.strip(), flags=re.S)
    try:
        return json.loads(t)
    except Exception:
        pass
    start = t.find("{")
    if start < 0:
        return None
    depth = 0; in_str = False; esc = False
    for i, ch in enumerate(t[start:], start):
        if in_str:
            if esc: esc = False
            elif ch == "\\": esc = True
            elif ch == '"': in_str = False
            continue
        if ch == '"': in_str = True
        elif ch == "{": depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                try:
                    return json.loads(t[start:i + 1])
                except Exception:
                    return None
    return None


def _style_summary(report: dict) -> dict | None:
    st = report.get("style") or {}
    if not st.get("season"):
        return None
    adv = st.get("advice") or {}
    return {"season": st["season"]["name"], "undertone": st["colors"]["skin"]["undertone"], "contrast": st["contrast"]["level"], "face_shape": st["face_shape"]["name"],
            "palette_best": [c["name"] for c in st["palette"]["best"]], "palette_avoid": [c["name"] for c in st["palette"]["avoid"]], "metals": st["palette"]["metals"],
            "hair_colors": st["palette"]["hair_colors"], "haircuts_suggested": [f"{h.get('name')}: {h.get('description')}" for h in adv.get("haircuts", [])][:4]}


async def build_async(report: dict) -> dict:
    intensity = assess_intensity(report)
    slim = {
        "profile": report.get("profile"), "quality_warnings": report.get("warnings"), "reference_group": report.get("norms", {}).get("group"),
        "intensity": intensity, "scores": report.get("scores"), "age": report.get("age"), "skin": {k: v for k, v in (report.get("skin") or {}).items() if k != "maps"},
        "parsing": report.get("parsing"), "profile_view": {k: v for k, v in (report.get("profile_view") or {}).items() if k in ("measures", "warnings")},
        "per_measure_percentiles": report.get("norms", {}).get("per_measure"),
        "style": _style_summary(report),
        "narrative": {k: {"summary": v.get("summary"), "watch": v.get("watch"), "strengths": v.get("strengths")} for k, v in (report.get("narrative") or {}).items() if not v.get("error")},
        "library": METHODS,
    }
    opts = ClaudeAgentOptions(system_prompt=SYSTEM, max_turns=1, allowed_tools=[], model=MODEL)
    text = ""
    async for msg in query(prompt=json.dumps(slim, ensure_ascii=False), options=opts):
        if isinstance(msg, AssistantMessage):
            for b in msg.content:
                if isinstance(b, TextBlock):
                    text += b.text
    data = extract_json(text)
    if data is None:
        data = {"phases": [], "not_recommended": [], "letter": text.strip()[:2000], "parse_error": True}
    valid = {x["id"] for x in METHODS}
    for ph in data.get("phases", []):
        ph["actions"] = [a for a in ph.get("actions", []) if a.get("method_id") in valid]
    data["intensity"] = intensity
    data.setdefault("expected_changes", []); data.setdefault("target_look", "")
    return data


def build(report: dict) -> dict:
    return anyio.run(build_async, report)
