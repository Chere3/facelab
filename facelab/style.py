"""Asesoría de estilo (Claude) y renders de looks (Codex) sobre la colorimetría.

- advise(report): armario por categorías, 6 looks (casual, smart casual, formal, urbano, más femenino, más masculino),
  4 cortes de pelo, 2–3 variantes de barba / cejas / maquillaje, colores de pelo y qué evitar. Cada sugerencia trae un
  render_prompt para editar la foto de busto.
- render_looks(report, out_dir, stem, ids): genera cada imagen con Codex image_gen en paralelo (3 a la vez).
"""
from __future__ import annotations
import json, os, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import anyio
from claude_agent_sdk import query, ClaudeAgentOptions, AssistantMessage, TextBlock
from .colorimetry import kb
from .protocol import extract_json, MODEL
from .visualize import _run, KEEP

OUTFIT_IDS = ["casual", "smart_casual", "formal", "urbano", "mas_femenino", "mas_masculino"]
STYLE_MEASURES = ["facial_index", "fwhr", "jaw_to_cheek", "chin_width_to_jaw", "eye_spacing_ratio", "brow_position", "brow_tilt", "canthal_tilt",
                  "lip_ratio", "mouth_width", "nasal_index", "facial_thirds", "lower_face_height", "symmetry"]

SYSTEM = """Eres asesor de imagen personal (colorimetría, estilismo y peluquería). Escribes en español, concreto y visual, sin adular.
Recibes la colorimetría medida en la foto (piel, pelo, ojos en LAB; estación de color con paleta; contraste; forma de cara), el perfil
declarado, la longitud de pelo actual, percentiles de medidas faciales y una base de conocimiento (cortes por forma de cara y expresión,
palancas de expresión femenina/masculina, reglas de prendas). Diseñas sugerencias para ESTA persona y devuelves SOLO JSON.
Reglas:
- Colores siempre de la paleta recibida (usa sus hex). Nunca recomiendes colores de la lista "avoid" salvo lejos de la cara y dilo.
- Cada sugerencia se justifica con un dato: estación, contraste, forma de cara, percentil o longitud de pelo actual.
- "expression": "neutral" respeta la expresión actual de la persona; "feminine" y "masculine" mueven las palancas de la base de conocimiento
  (pelo, cejas, contraste, barba, cuellos, monturas, accesorios) de forma creíble y realista para ella. No son juicios ni cambios de identidad.
- Los 6 outfits usan exactamente estos ids: casual, smart_casual, formal, urbano, mas_femenino, mas_masculino. Los dos últimos son un look
  diario con expresión feminine y masculine respectivamente. Cada uno: 3–5 prendas con color (hex de la paleta) y corte, 1–3 accesorios
  (gafas con forma de montura si procede, reloj/joyas con el metal de la paleta, gorra/sombrero, bufanda), y grooming (pelo, barba o maquillaje) coherente.
- 4 cortes de pelo (ids corte_1..corte_4): dos en la expresión actual (uno conservador, uno más atrevido), uno feminine y uno masculine.
  Descríbelos como lo haría un peluquero: largo en cm arriba y laterales, raya, textura, flequillo, cómo se peina, mantenimiento.
  Ten en cuenta el largo actual (si es corto, un corte largo exige meses: dilo en "maintenance").
- grooming (2–3, ids libres como barba_corta, barba_completa, afeitado, cejas_definidas, maquillaje_contraste): barba solo si hay sexo male o expresión masculine;
  maquillaje solo con expresión feminine o sexo female. Siempre realistas.
- "render_prompt": instrucción visual precisa en español para un editor de imagen que edita la foto de busto: qué prendas (tipo, color por nombre y hex, cuello),
  qué accesorios, y qué peinado/barba/maquillaje. Solo describe lo que cambia. Sin nombres de marca.
Devuelve SOLO este JSON:
{"summary":"3–5 frases: estación, contraste, forma de cara y qué significa para vestir",
 "color_story":"2–3 frases sobre cómo combinar la paleta (neutros base + acentos, metales, estampados)",
 "wardrobe":[{"category":"camisas y camisetas|jerséis y sudaderas|chaquetas y abrigos|pantalones|calzado|gafas|reloj y joyería|gorras y sombreros|bufandas y pañuelos","picks":["prenda concreta con color y por qué"],"avoid":["..."]}],
 "outfits":[{"id":"casual","name":"","occasion":"","expression":"neutral","pieces":["..."],"colors":["#hex"],"accessories":["..."],"grooming":"","why":"","render_prompt":""}],
 "haircuts":[{"id":"corte_1","name":"","expression":"neutral|feminine|masculine","description":"","maintenance":"","why":"","render_prompt":""}],
 "grooming":[{"id":"","name":"","expression":"","description":"","why":"","render_prompt":""}],
 "hair_color":["opciones de color de pelo de la paleta con por qué, o 'mantener el natural' con por qué"],
 "avoid":["5–8 cosas concretas que no favorecen y por qué"]}"""


def _payload(report: dict) -> dict:
    st = report.get("style") or {}
    K = kb(); season = K["seasons"].get(st.get("season", {}).get("id"), {}); sec = K["seasons"].get(st.get("season", {}).get("secondary_id"), {})
    shape = K["face_shapes"].get((st.get("face_shape") or {}).get("id"), {})
    per = (report.get("norms") or {}).get("per_measure") or {}
    pcts = {k: v.get("percentile") for k, v in per.items() if k.split(".")[0] in STYLE_MEASURES and v.get("percentile") is not None}
    narr = report.get("narrative") or {}
    return {
        "profile": report.get("profile"), "visual_age": (report.get("age") or {}).get("visual_age"),
        "colorimetry": {k: st.get(k) for k in ("colors", "axes", "contrast", "chroma", "season", "palette", "face_shape", "hair", "note")},
        "parsing": {k: (report.get("parsing") or {}).get(k) for k in ("glasses", "hat", "hair_visible")},
        "percentiles": pcts,
        "narrative_hints": {k: {"strengths": v.get("strengths", [])[:2], "watch": v.get("watch", [])[:2]} for k, v in narr.items() if not v.get("error")},
        "protocol_target_look": (report.get("protocol") or {}).get("target_look"),
        "knowledge": {"season": season, "secondary_season": {"name": sec.get("name"), "summary": sec.get("summary")}, "contrast_rules": K["contrast_rules"],
                      "face_shape": shape, "expression": K["expression"], "garment_rules": K["garment_rules"]},
    }


async def advise_async(report: dict) -> dict:
    opts = ClaudeAgentOptions(system_prompt=SYSTEM, max_turns=1, allowed_tools=[], model=MODEL)
    text = ""
    async for msg in query(prompt=json.dumps(_payload(report), ensure_ascii=False), options=opts):
        if isinstance(msg, AssistantMessage):
            for b in msg.content:
                if isinstance(b, TextBlock):
                    text += b.text
    data = extract_json(text)
    if data is None:
        return {"parse_error": True, "raw": text.strip()[:2000]}
    for k in ("wardrobe", "outfits", "haircuts", "grooming", "hair_color", "avoid"):
        data.setdefault(k, [])
    return data


def advise(report: dict) -> dict:
    return anyio.run(advise_async, report)


# ---------- renders ----------

def render_items(report: dict) -> list[dict]:
    """Todas las sugerencias renderizables: outfits, cortes y grooming, con su tipo."""
    adv = ((report.get("style") or {}).get("advice")) or {}
    items = [{**o, "kind": "outfit"} for o in adv.get("outfits", [])] + [{**h, "kind": "haircut"} for h in adv.get("haircuts", [])] + [{**g, "kind": "grooming"} for g in adv.get("grooming", [])]
    return [i for i in items if i.get("id") and i.get("render_prompt")]


def _wrap(item: dict, out_name: str, report: dict) -> str:
    scope = {"outfit": "Cambia solo la ropa, los accesorios y, si el encargo lo dice, el peinado, la barba o el maquillaje. Muestra hombros y parte alta del torso; si la foto los recorta, amplía ligeramente el encuadre hacia abajo. Puedes sustituir el fondo por uno neutro liso si el original estorba.",
             "haircut": "Cambia solo el pelo: corte, largo, textura, raya, flequillo y, si el encargo lo dice, el color. Ropa, fondo y todo lo demás quedan idénticos.",
             "grooming": "Cambia solo lo que dice el encargo (barba, cejas o maquillaje). Pelo, ropa y fondo quedan idénticos."}[item["kind"]]
    age = (report.get("age") or {}).get("visual_age")
    return (f"Edita la foto adjunta. Es la MISMA persona y debe reconocerse al instante: conserva {KEEP}. "
            + (f"Su edad aparente es de unos {age} años y debe seguir pareciendo esa edad. " if age else "")
            + f"{scope} Resultado fotográfico realista, sin filtros de belleza, sin adelgazar ni cambiar huesos, nariz u ojos. "
            f"ENCARGO ({item.get('name', item['id'])}): {item['render_prompt']} "
            f"Guarda el PNG resultante en el directorio de trabajo actual con el nombre exacto {out_name}. No escribas nada más que la confirmación.")


def preview(out_dir: Path, png_name: str, width: int = 720) -> str:
    """JPEG de vista previa (el PNG de Codex pesa ~2 MB; el informe y el PDF usan el JPEG)."""
    import cv2
    im = cv2.imread(str(out_dir / png_name))
    if im is None:
        return png_name
    s = width / im.shape[1]
    if s < 1:
        im = cv2.resize(im, None, fx=s, fy=s, interpolation=cv2.INTER_AREA)
    name = png_name[:-4] + ".jpg"; cv2.imwrite(str(out_dir / name), im, [cv2.IMWRITE_JPEG_QUALITY, 86]); return name


def render_looks(report: dict, out_dir: Path, stem: str, ids: list[str] | None = None, on_progress=None, timeout: int = 420) -> dict:
    st = report.setdefault("style", {})
    renders = st.setdefault("renders", {})
    items = render_items(report)
    if ids:
        items = [i for i in items if i["id"] in set(ids)]
    if not items:
        raise RuntimeError("no hay sugerencias con render_prompt (falta la asesoría de estilo)")
    base = out_dir / (st.get("bust") or report["assets"]["face"])
    if not base.exists():
        base = out_dir / report["assets"]["face"]
    done = 0

    def one(item):
        nonlocal done
        name = f"{stem}_look_{item['id']}.png"; prompt = _wrap(item, name, report)
        try:
            (out_dir / name).unlink(missing_ok=True)
            _run(prompt, base, out_dir, name, timeout)
            renders[item["id"]] = {"file": preview(out_dir, name), "png": name, "kind": item["kind"], "prompt": prompt, "ts": int(time.time())}
        except Exception as e:
            renders[item["id"]] = {"file": None, "kind": item["kind"], "prompt": prompt, "error": str(e)[:300], "ts": int(time.time())}
        done += 1
        if on_progress:
            on_progress(done, len(items))

    with ThreadPoolExecutor(max_workers=int(os.environ.get("FACELAB_LOOK_PARALLEL", "3"))) as ex:
        list(ex.map(one, items))
    return renders
