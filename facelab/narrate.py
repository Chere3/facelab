"""Narrativa por sección con Claude (Agent SDK, sesión de Claude Code; sin API key).

Cada sección se redacta en un agente independiente con solo sus medidas, percentiles y normas.
Salida: dict {section: {summary, findings[], strengths[], watch[]}} en español, registro clínico y contenido.
"""
from __future__ import annotations
import asyncio, json
import anyio
from claude_agent_sdk import query, ClaudeAgentOptions, AssistantMessage, TextBlock
from .measures import CATALOG_BY_ID

MODEL = "claude-sonnet-5"

SECTIONS = {
    "proporciones": ["facial_thirds", "facial_fifths", "facial_index", "fwhr", "midface_ratio"],
    "ojos_y_cejas": ["eye_width", "eye_height", "eye_aspect_ratio", "canthal_tilt", "eye_spacing_ratio",
                     "intercanthal_width", "interpupillary_distance", "brow_position", "brow_tilt"],
    "nariz": ["nose_width", "nasal_height", "nasal_index", "nose_to_intercanthal", "sagittal_angles"],
    "perfil": [],
    "boca_y_labios": ["mouth_width", "mouth_to_nose", "philtrum_length", "lip_ratio", "lip_height_to_mouth_width", "commissure_tilt"],
    "tercio_inferior": ["lower_face_height", "chin_height", "chin_to_lower_face", "bigonial_width", "bizygomatic_width",
                        "jaw_to_cheek", "chin_width_to_jaw"],
    "global": ["symmetry"],
}

SYSTEM = """Eres un analista de morfometría facial. Redactas en español, en registro clínico, sobrio y concreto.
Reglas:
- Describe medidas, no juzgues el atractivo ni el valor de la persona. Nada de "bonito", "feo", "ideal" salvo citando una norma.
- Cada afirmación numérica debe apoyarse en el dato que recibes (valor, percentil dentro de su grupo demográfico, norma citada).
- Cuando una medida trae "caveat", di explícitamente que es orientativa y por qué.
- Percentil 40-60 = típico; 25-40 o 60-75 = ligeramente por debajo/encima; <25 o >75 = claramente por debajo/encima. No inventes rangos.
- Si el grupo de referencia no coincide con la ascendencia declarada (p. ej. "male|all"), menciónalo.
- No recomiendes cirugía ni productos. Como mucho, señala qué rasgos merecen atención y cuáles son puntos fuertes.
- Devuelve SOLO un JSON con esta forma exacta:
{"summary": "2-4 frases", "findings": [{"measure": "id", "statement": "1-2 frases con el dato"}], "strengths": ["..."], "watch": ["..."]}"""


def _section_payload(report: dict, keys: list[str]) -> dict:
    per = report.get("norms", {}).get("per_measure", {})
    out = {}
    for k in keys:
        m = report["measures"].get(k)
        if not m:
            continue
        cat = CATALOG_BY_ID.get(k, {})
        entry = {"name": cat.get("name"), "value": m["value"], "unit": m["unit"], "norm": cat.get("norm"),
                 "formula": cat.get("formula")}
        if m.get("caveat"):
            entry["caveat"] = m["caveat"]
        if m["unit"] == "px":
            entry["caveat"] = "valor en píxeles de esta foto: no comparable con otras personas; úsalo solo dentro de los ratios"
        stats = {kk: v for kk, v in per.items() if kk == k or kk.startswith(k + ".")}
        if stats:
            entry["group_stats"] = stats
        out[k] = entry
    return out


async def _ask(section: str, payload: dict, profile: dict, group: str, extras: dict | None, retries: int = 1) -> tuple[str, dict]:
    """Una sección; ante fallo del CLI reintenta una vez y, si persiste, devuelve un bloque de error sin tumbar al resto."""
    for attempt in range(retries + 1):
        try:
            return await _ask_once(section, payload, profile, group, extras)
        except Exception as e:
            if attempt >= retries:
                return section, {"summary": "", "findings": [], "strengths": [], "watch": [], "error": f"{type(e).__name__}: {str(e)[:200]}"}
            await asyncio.sleep(2)


async def _ask_once(section: str, payload: dict, profile: dict, group: str, extras: dict | None) -> tuple[str, dict]:
    prompt = json.dumps({"section": section, "profile": profile, "reference_group": group, "measures": payload,
                         "global_scores": extras or {}}, ensure_ascii=False)
    opts = ClaudeAgentOptions(system_prompt=SYSTEM, max_turns=1, allowed_tools=[], model=MODEL)
    text = ""
    async for msg in query(prompt=prompt, options=opts):
        if isinstance(msg, AssistantMessage):
            for b in msg.content:
                if isinstance(b, TextBlock):
                    text += b.text
    from .protocol import extract_json
    data = extract_json(text)
    if data is None:
        return section, {"summary": text.strip()[:2000], "findings": [], "strengths": [], "watch": [], "parse_error": True}
    return section, data


async def narrate_async(report: dict) -> dict:
    profile = report.get("profile", {})
    pv = report.get("profile_view")
    group = report.get("norms", {}).get("group", "all|all")
    scores = report.get("scores", {})
    results = {}
    async with anyio.create_task_group() as tg:
        async def run(section, keys):
            extras = scores if section == "global" else None
            s, r = await _ask(section, _section_payload(report, keys), profile, group, extras)
            results[s] = r
        for section, keys in SECTIONS.items():
            if section == "perfil":
                if not pv:
                    continue
                async def run_profile():
                    payload = {k: {"name": k, "value": v["value"], "unit": "deg" if "ratio" not in k and "eline" not in k else "ratio", "norm": {"range": v.get("range"), "source": v.get("source")}} for k, v in pv["measures"].items()}
                    payload["_note"] = "Medidas reales de una foto de perfil (silueta por segmentación). Las distancias E-line y proyecciones están normalizadas por N–Me (sin mm)."
                    s, r = await _ask("perfil", payload, profile, group, None); results[s] = r
                tg.start_soon(run_profile); continue
            tg.start_soon(run, section, keys)
    return {s: results[s] for s in SECTIONS if s in results}


def narrate(report: dict) -> dict:
    return anyio.run(narrate_async, report)
