"""Visualización con Codex (image_gen, gpt-5.5) basada en el protocolo y en las estadísticas del sujeto.

- El "look objetivo" del protocolo (target_look) y sus acciones definen los cambios.
- Los percentiles y mapas de piel añaden cambios concretos (targeted_edits).
- En nivel glow-up se generan dos imágenes: 3 meses (cambios tempranos) y 12 meses (look objetivo completo).
"""
from __future__ import annotations
import subprocess, shutil
from pathlib import Path

CODEX_MODEL = "gpt-5.5"
KEEP = "la identidad (sus amigos deben reconocerle al instante), la estructura ósea, la forma y el tamaño de nariz, ojos, cejas, labios, orejas, mandíbula y mentón, la distancia entre los ojos, el color de piel y de ojos, la edad aparente, la expresión, el encuadre, el fondo y la luz"
EARLY_IDS = {"sunscreen_daily", "vitamin_c_am", "niacinamide", "azelaic_acid", "hydration_barrier", "brow_shaping", "brow_redesign", "lash_serum", "lash_lift_tint",
             "under_eye_routine", "haircut_face_shape", "hair_transformation", "hair_color", "beard_shaping", "sleep_hygiene", "sleep_recovery_program", "sodium_alcohol",
             "teeth_whitening", "lip_care", "eyewear_or_contacts", "glasses_frames", "style_color_palette", "makeup_grooming_basics", "hat_uv_avoidance", "photo_technique", "posture_head"}
ACTION_HINTS = {
    "retinoid_night": "piel más lisa y uniforme, poros menos visibles", "sunscreen_daily": "tono de piel más parejo", "vitamin_c_am": "piel más luminosa",
    "niacinamide": "menos rojez y poros más finos", "azelaic_acid": "menos rojez", "aha_bha_exfoliation": "textura más lisa", "hydration_barrier": "piel hidratada",
    "brow_shaping": "cejas perfiladas con arco limpio y cola definida", "brow_redesign": "cejas rediseñadas, más densas y con arco definido", "brow_growth_serum": "cejas más densas",
    "brow_lamination": "cejas ordenadas con cuerpo", "lash_serum": "pestañas más densas", "lash_lift_tint": "pestañas curvadas y oscuras", "under_eye_routine": "ojeras atenuadas",
    "haircut_face_shape": "corte de pelo pulido que equilibra sus proporciones", "hair_transformation": "pelo transformado según el look objetivo", "hair_color": "color de pelo según el look objetivo",
    "beard_shaping": "barba perfilada que define la mandíbula", "beard_growth_program": "barba completa y perfilada que define la mandíbula", "body_fat_reduction": "rostro más definido",
    "body_recomposition": "rostro claramente más definido, menos grasa en mejillas y bajo el mentón, cuello más marcado", "sleep_hygiene": "aspecto descansado", "sleep_recovery_program": "aspecto descansado, ojos sin hinchazón",
    "sodium_alcohol": "cara menos hinchada", "teeth_whitening": "dientes más blancos", "dental_full": "dientes blancos y alineados", "lip_care": "labios hidratados",
    "tranexamic_topical": "manchas atenuadas", "benzoyl_peroxide": "sin granos", "chemical_peel_pro": "textura de piel muy lisa", "microneedling": "cicatrices atenuadas",
    "laser_vascular": "sin rojez ni capilares", "skin_pro_program": "piel visiblemente más lisa, uniforme y sin rojez", "scalp_hair_care": "pelo más denso", "makeup_grooming_basics": "grooming cuidado",
    "smoking_alcohol_reduction": "piel más fresca", "eyewear_or_contacts": "sin gafas o con montura que enmarca bien los ojos (según el look objetivo)", "glasses_frames": "montura que enmarca bien los ojos",
    "style_color_palette": "ropa en colores que favorecen su tono de piel", "posture_neck_program": "cabeza erguida, cuello más largo y mandíbula más definida", "posture_head": "cabeza erguida",
    "botox_pro": "frente y entrecejo relajados, sin arrugas de expresión", "filler_pro": "zona tratada con volumen sutil según el look objetivo", "mewing_no": "",
}


def _pct(report, key):
    pm = (report.get("norms") or {}).get("per_measure") or {}
    if key in pm:
        return pm[key].get("percentile")
    vals = [v.get("percentile") for k, v in pm.items() if k.startswith(key + ".") and v.get("percentile") is not None]
    return sum(vals) / len(vals) if vals else None


def targeted_edits(report: dict) -> list[str]:
    prof = report.get("profile") or {}; sex = prof.get("sex"); edits = []
    sk = (report.get("skin") or {}).get("percentiles") or {}
    sp = lambda k: (sk.get(k) or {}).get("percentile")
    if (sp("spots_pct") or 0) > 60: edits.append("tono de piel uniforme, manchas y sombras atenuadas")
    if (sp("redness_pct") or 0) > 60: edits.append("menos rojez en mejillas y nariz")
    if (sp("texture_index") or 0) > 60: edits.append("textura de piel lisa, poros menos visibles")
    if (sp("shine_pct") or 0) > 70: edits.append("piel matificada")
    bp = _pct(report, "brow_position")
    if bp is not None and bp < 25: edits.append("arco de las cejas ligeramente más elevado y definido")
    ear = _pct(report, "eye_aspect_ratio")
    if ear is not None and ear < 20: edits.append("mirada más descansada y abierta, sin cambiar la forma del ojo")
    fi = _pct(report, "facial_index")
    if fi is not None and fi > 80: edits.append("pelo con volumen lateral y poca altura, que ensancha visualmente la cara")
    elif fi is not None and fi < 20: edits.append("pelo con altura y laterales cortos, que alarga visualmente la cara")
    jc = _pct(report, "jaw_to_cheek")
    if sex == "male" and jc is not None and jc < 30: edits.append("barba corta y perfilada que define la mandíbula")
    age = (report.get("age") or {}).get("visual_age"); declared = prof.get("age")
    if age and declared and age > declared + 5: edits.append("aspecto más descansado y fresco, sin rejuvenecer artificialmente")
    return list(dict.fromkeys(edits))


def _actions(report):
    return [a for ph in (report.get("protocol") or {}).get("phases", []) for a in ph.get("actions", [])]


def build_prompt(report: dict, out_name: str, horizon: str) -> str:
    P = report.get("protocol") or {}
    tier = (P.get("intensity") or {}).get("tier", "mejora")
    acts = _actions(report)
    if horizon == "3m":
        acts = [a for a in acts if a.get("method_id") in EARLY_IDS]
    hints = [ACTION_HINTS.get(a.get("method_id")) for a in acts]
    hints = [h for h in hints if h]
    specs = [f"{a.get('name')}: {a.get('spec')}" for a in acts if a.get("spec")]
    edits = targeted_edits(report)
    look = P.get("target_look", "")
    prof = report.get("profile") or {}
    strength = {"glow-up": "Los cambios deben notarse claramente (es una transformación de 12 meses), pero todo debe ser alcanzable sin cirugía: pelo, barba o cejas, piel, definición facial por pérdida de grasa, dientes, gafas y ropa.",
                "mejora": "Cambios claros pero moderados.", "mantenimiento": "Cambios muy sutiles."}[tier]
    if horizon == "3m":
        strength = "Es el resultado a 3 meses: solo lo que cambia rápido (piel más cuidada, cejas, corte y color de pelo, barba perfilada, descanso, gafas). Sin cambios de composición corporal ni dentales todavía."
    age = (report.get("age") or {}).get("visual_age")
    st = report.get("style") or {}
    palette = ("Ropa en colores de su paleta (" + st["season"]["name"] + "): " + ", ".join(c["name"] for c in st["palette"]["best"][:5]) + "; evitar " + ", ".join(c["name"] for c in st["palette"]["avoid"][:3]) + ". ") if st.get("palette") else ""
    return (
        f"Edita la foto adjunta. Es la MISMA persona y debe reconocerse al instante: conserva {KEEP}. "
        + (f"Su edad aparente es de unos {age} años y debe seguir pareciendo esa edad. " if age else "")
        + "Trabaja como un retocador: cambia solo pelo, vello facial, cejas, piel, grasa facial, dientes, gafas y ropa; todo lo demás queda idéntico píxel a píxel en lo posible. "
        f"Perfil: {prof.get('sex') or 'sin sexo'}, {prof.get('ancestry') or 'sin ascendencia'}, nivel de protocolo {tier}. {strength} "
        + (f"LOOK OBJETIVO al que debe parecerse el resultado: {look} " if look and horizon != "3m" else "")
        + ("Cambios a aplicar: " + "; ".join(dict.fromkeys(hints + edits)) + ". " if (hints or edits) else "")
        + ("Detalles ejecutables: " + " | ".join(specs[:8]) + ". " if specs and horizon != "3m" else "")
        + palette
        + "Prohibido: adelgazar o cambiar huesos, alterar nariz u ojos, blanquear la piel, rejuvenecer artificialmente, filtros de belleza. "
        f"Guarda el PNG resultante en el directorio de trabajo actual con el nombre exacto {out_name}. No escribas nada más que la confirmación."
    )


def _run(prompt: str, face: Path, out_dir: Path, out_name: str, timeout: int):
    proc = subprocess.run(["codex", "exec", "-m", CODEX_MODEL, "--skip-git-repo-check", "-s", "workspace-write", "-i", str(face), "-"],
                          input=prompt, text=True, capture_output=True, cwd=str(out_dir), timeout=timeout)
    if not (out_dir / out_name).exists():
        raise RuntimeError("Codex no generó la imagen: " + (proc.stdout[-600:] + proc.stderr[-300:]).strip())


def generate(report: dict, out_dir: Path, stem: str, timeout: int = 420) -> dict:
    if not shutil.which("codex"):
        raise RuntimeError("codex CLI no encontrado")
    face = out_dir / report["assets"]["face"]
    tier = ((report.get("protocol") or {}).get("intensity") or {}).get("tier", "mejora")
    out = {"model": CODEX_MODEL, "tier": tier, "edits": targeted_edits(report)}
    name12 = f"{stem}_after.png"
    src12 = face
    if tier == "glow-up":
        # primero 3 meses desde la foto original; después 12 meses editando la de 3 meses (encadenar conserva mejor la identidad)
        name3 = f"{stem}_after_3m.png"; p3 = build_prompt(report, name3, "3m")
        try:
            _run(p3, face, out_dir, name3, timeout); out["after_3m"] = name3; out["prompt_3m"] = p3; src12 = out_dir / name3
        except Exception as e:
            out["after_3m_error"] = str(e)[:200]
    p12 = build_prompt(report, name12, "12m"); _run(p12, src12, out_dir, name12, timeout)
    out["after"] = name12; out["prompt"] = p12; out["chained"] = str(src12) != str(face)
    return out
