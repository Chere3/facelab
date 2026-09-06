"""Servidor local: sube fotos, elige perfil, ve medidas con percentiles, scores y narrativa de Claude.

uv run python -m facelab.serve   →  http://localhost:8766
Fotos en samples/mine/, resultados en out/mine/.
"""
from __future__ import annotations
import json, os, re, time
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from .measures import CATALOG_BY_ID
from .profile import Profile

ROOT = Path(__file__).resolve().parent.parent
IN_DIR, OUT_DIR = ROOT / "samples" / "mine", ROOT / "out" / "mine"
app = FastAPI(title="facelab")


def _sanitize(o):
    """NaN/Inf → None para que la respuesta JSON sea válida."""
    import math
    if isinstance(o, float):
        return None if (math.isnan(o) or math.isinf(o)) else o
    if isinstance(o, dict):
        return {k: _sanitize(v) for k, v in o.items()}
    if isinstance(o, list):
        return [_sanitize(v) for v in o]
    return o

PAGE = """<!doctype html><meta charset="utf-8"><title>facelab</title>
<style>
body{font:15px/1.5 -apple-system,system-ui,sans-serif;max-width:1180px;margin:32px auto;padding:0 20px;color:#171c1e;background:#f3f4f1}
h1{font-size:22px;margin:0 0 4px}h2{font-size:17px;margin:28px 0 8px}p.sub{color:#5b6569;margin:0 0 16px}
form.prof{display:flex;gap:14px;flex-wrap:wrap;align-items:end;margin:0 0 14px;font-size:13px}label{display:flex;flex-direction:column;gap:3px;color:#5b6569}
select,input[type=number]{font:14px system-ui;padding:5px 8px;border:1px solid #cfd6d2;border-radius:4px;background:#fff}
#drop{border:2px dashed #9aa8a5;padding:32px;text-align:center;border-radius:6px;background:#e9ecea;cursor:pointer}#drop.over{background:#d5e8e6;border-color:#1f6b6a}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:1px;background:#cfd6d2;border:1px solid #cfd6d2;margin:16px 0}
.tiles div{background:#e9ecea;padding:12px}.tiles b{display:block;font-size:26px;font-variant-numeric:tabular-nums}.tiles small{color:#5b6569;font-size:12px;line-height:1.35;display:block}
.row{display:grid;grid-template-columns:minmax(0,1fr) 360px;gap:24px}@media(max-width:800px){.row{grid-template-columns:1fr}}
table{border-collapse:collapse;width:100%;font-size:13px}th{text-align:left;font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:#5b6569;padding:6px 8px;border-bottom:1px solid #171c1e}
td{padding:6px 8px;border-bottom:1px solid #cfd6d2;vertical-align:top;font-variant-numeric:tabular-nums}td.v{font-family:ui-monospace,Menlo,monospace;white-space:nowrap}
.pct{display:inline-block;min-width:44px;text-align:right;font-family:ui-monospace,Menlo,monospace}.lo{color:#b8741a}.hi{color:#1f6b6a}
img{max-width:100%;border:1px solid #cfd6d2}.warn{background:#f1e3cc;border-left:3px solid #b8741a;padding:8px 12px;margin:12px 0}
.q{font-family:ui-monospace,Menlo,monospace;font-size:12px;color:#5b6569}
button{font:14px system-ui;padding:8px 14px;border:1px solid #1f6b6a;background:#1f6b6a;color:#fff;border-radius:4px;cursor:pointer}button[disabled]{opacity:.5}
.sec{border-left:3px solid #1f6b6a;background:#e9ecea;padding:12px 16px;margin:12px 0}.sec h3{margin:0 0 6px;font-size:15px}.sec ul{margin:6px 0;padding-left:20px}
</style>
<h1>facelab</h1><p class="sub">Foto frontal, mirada a cámara, luz uniforme, sin gafas, boca en reposo (una sonrisa distorsiona boca, labios y proporcionalidad). Al subirla se genera el informe completo: medidas, narrativa, protocolo y visualización.</p><p class="sub" id="prev"></p><p class="sub"><a href="/admin">Cola de revisión</a> · <a href="/people">Personas y seguimiento</a></p>
<form class="prof" onsubmit="return false">
 <label>Sexo<select id="sex"><option value="">sin especificar</option><option value="male">hombre</option><option value="female">mujer</option></select></label>
 <label>Ascendencia (grupo de referencia)<select id="anc"><option value="">sin especificar</option><option value="hispanic">hispana / latina</option><option value="caucasian">caucásica</option><option value="asian">asiática</option><option value="black">negra / africana</option><option value="indian">india / sur de Asia</option><option value="mideastern">medio-oriental</option><option value="other">otra / mixta</option></select></label>
 <label>Edad<input id="age" type="number" min="10" max="99" style="width:70px"></label>
 <label>Ambición del protocolo<select id="amb"><option value="">automática (según hallazgos)</option><option value="mejora">mejora</option><option value="glow-up">glow-up (12 meses, radical)</option></select></label>
 <label>Nombre o email (para seguimiento)<input id="person" type="text" style="width:220px;font:14px system-ui;padding:5px 8px;border:1px solid #cfd6d2;border-radius:4px"></label>
 <label>Foto de perfil (opcional, 90°)<input id="pf" type="file" accept="image/*"></label>
</form>
<div id="drop">Arrastra una foto aquí o haz clic para elegirla<input id="f" type="file" accept="image/*" hidden></div>
<div id="res"></div>
<script>
fetch('/reports').then(r=>r.json()).then(l=>{if(l.length)document.getElementById('prev').innerHTML='Informes anteriores: '+l.slice(0,8).map(x=>'<a href="/report/'+x.stem+'">'+x.stem+'</a>').join(' · ')});
const d=document.getElementById('drop'),f=document.getElementById('f'),res=document.getElementById('res');let last=null;
d.onclick=()=>f.click();d.ondragover=e=>{e.preventDefault();d.classList.add('over')};d.ondragleave=()=>d.classList.remove('over');
d.ondrop=e=>{e.preventDefault();d.classList.remove('over');send(e.dataTransfer.files[0])};f.onchange=()=>send(f.files[0]);
const fmt=v=>typeof v==='object'&&v!==null?Object.entries(v).map(([a,b])=>a+' '+b).join(' · '):v;
const pct=p=>p==null?'':'<span class="pct '+(p<25?'lo':p>75?'hi':'')+'">p'+Math.round(p)+'</span>';
async function send(file){if(!file)return;res.innerHTML='<p>Subiendo… el informe se abre enseguida y se completa solo (≈3–5 min).</p>';const fd=new FormData();fd.append('file',file);
fd.append('sex',document.getElementById('sex').value);fd.append('ancestry',document.getElementById('anc').value);fd.append('age',document.getElementById('age').value);fd.append('person',document.getElementById('person').value);fd.append('ambition',document.getElementById('amb').value);const pf=document.getElementById('pf').files[0];if(pf)fd.append('profile_photo',pf);
const r=await fetch('/analyze',{method:'POST',body:fd});const j=await r.json();if(j.error){res.innerHTML='<div class="warn">'+j.error+'</div>';return}location.href=j.report_url}
function render(j){const s=j.scores||{},pm=(j.norms||{}).per_measure||{};
let h='<div class="q">yaw '+j.quality.yaw_deg+'° · pitch '+j.quality.pitch_deg+'° · roll '+j.quality.roll_deg+'° · nitidez '+j.quality.blur_laplacian_var+' · grupo de referencia '+((j.norms||{}).group||'-')+' (n='+((j.norms||{}).n||0)+')</div>';
for(const w of j.warnings)h+='<div class="warn">'+w+'</div>';
if(s.symmetry){h+='<div class="tiles">';
h+='<div><b>'+s.symmetry.score+'</b><small>Simetría · percentil '+s.symmetry.percentile+' (media grupo '+s.symmetry.group_mean+')</small></div>';
h+='<div><b>'+s.averageness.score+'</b><small>Averageness · 100 = más cerca de la forma media del grupo</small></div>';
h+='<div><b>'+s.dimorphism.masculinity_index+'</b><small>Índice de masculinidad · 0 = media femenina, 100 = media masculina · percentil '+s.dimorphism.percentile_within_sex+' dentro de tu sexo</small></div>';
h+='<div><b>'+s.proportionality.score+'</b><small>Proporcionalidad · 100 = 17 ratios más cerca de la media del grupo</small></div></div>'}
h+='<p><a href="/report/'+j.json_path.split('/').pop().replace('.json','')+'"><button>Ver informe completo</button></a> <button class="ghost" id="nar" onclick="narrate()" style="background:#fff;color:#1f6b6a">Generar narrativa aquí (≈1 min)</button></p><div id="narr"></div>';
h+='<div class="row"><div><table><tr><th>Medida</th><th>Valor</th><th>Percentil</th><th>Norma</th></tr>';
for(const [k,v] of Object.entries(j.measures)){const c=j.catalog[k]||{};let p='';if(typeof v.value==='object'&&v.value){p=Object.keys(v.value).map(kk=>pm[k+'.'+kk]?kk+' '+pct(pm[k+'.'+kk].percentile):'').join(' ')}else if(pm[k])p=pct(pm[k].percentile);
h+='<tr><td>'+(c.name||k)+'</td><td class="v">'+fmt(v.value)+' <span class="q">'+(v.unit||'')+'</span></td><td>'+p+'</td><td class="q">'+(c.norm&&c.norm!=='none'?JSON.stringify(c.norm).replace(/[{}"]/g,'').replace(/,/g,', '):'')+'</td></tr>'}
h+='</table></div><div><img src="'+j.debug_url+'"><p class="q">JSON: '+j.json_path+'</p></div></div>';res.innerHTML=h;if(j.narrative)showNarr(j.narrative)}
async function narrate(){const b=document.getElementById('nar');b.disabled=true;b.textContent='Redactando…';
const r=await fetch('/narrate',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({json_path:last.json_path})});const j=await r.json();
if(j.error){document.getElementById('narr').innerHTML='<div class="warn">'+j.error+'</div>'}else{last.narrative=j.narrative;showNarr(j.narrative)}b.disabled=false;b.textContent='Regenerar informe'}
function showNarr(n){let h='';for(const [s,r] of Object.entries(n)){h+='<div class="sec"><h3>'+s.replace(/_/g,' ')+'</h3><p>'+(r.summary||'')+'</p>';
if(r.findings&&r.findings.length)h+='<ul>'+r.findings.map(f=>'<li><b>'+f.measure+'</b>: '+f.statement+'</li>').join('')+'</ul>';
if(r.strengths&&r.strengths.length)h+='<p><b>Puntos fuertes:</b> '+r.strengths.join(' · ')+'</p>';if(r.watch&&r.watch.length)h+='<p><b>Atención:</b> '+r.watch.join(' · ')+'</p>';h+='</div>'}document.getElementById('narr').innerHTML=h}
</script>"""


@app.get("/", response_class=HTMLResponse)
def index():
    from .landing_page import PAGE as LANDING
    return LANDING


@app.get("/classic", response_class=HTMLResponse)
def classic():
    return PAGE


@app.get("/feed", response_class=HTMLResponse)
def feed_page():
    from .feed_page import PAGE as FEED
    return FEED


@app.get("/api/feed")
def api_feed():
    """Resumen público de cada informe (los marcados feed=false quedan fuera)."""
    items = []
    for p in sorted(OUT_DIR.glob("*.json"), key=lambda x: x.stat().st_mtime, reverse=True):
        if p.name.endswith((".status.json", ".meta.json")):
            continue
        try:
            d = json.loads(p.read_text(), parse_constant=lambda c: None)
        except json.JSONDecodeError:
            continue
        if d.get("feed") is False or not d.get("assets", {}).get("face"):
            continue
        sc = d.get("scores") or {}; st = d.get("style") or {}; G = (sc.get("global") or {}).get("composite") or {}
        strengths = [x for v in (d.get("narrative") or {}).values() for x in (v.get("strengths") or [])[:1]]
        summary = ((d.get("narrative") or {}).get("global") or {}).get("summary") or ""
        items.append(_sanitize({
            "stem": p.stem, "name": d.get("person") or None, "date": d.get("date"), "face": d["assets"]["face"], "profile": d.get("profile"),
            "global": G.get("score"), "symmetry": (sc.get("symmetry") or {}).get("score"), "proportionality": (sc.get("proportionality") or {}).get("score"),
            "averageness": (sc.get("averageness") or {}).get("score"), "visual_age": (d.get("age") or {}).get("visual_age"),
            "season": (st.get("season") or {}).get("name"), "season_hex": ((st.get("palette") or {}).get("best") or [{}])[0].get("hex"),
            "face_shape": (st.get("face_shape") or {}).get("name"), "strength": strengths[0] if strengths else summary[:160],
            "headline": _headline(st, sc), "reviewed": bool((d.get("review") or {}).get("approved")),
            "after": (d.get("visualization") or {}).get("after"), "look": next((v.get("file") for v in ((st.get("renders") or {}).values()) if v.get("file")), None),
        }))
    return items


def _headline(st: dict, sc: dict) -> str | None:
    season, shape = (st.get("season") or {}).get("name"), (st.get("face_shape") or {}).get("name")
    if season and shape:
        return f"{season}, cara {shape.lower()}"
    sym = (sc.get("symmetry") or {}).get("percentile")
    return f"Simetría en el percentil {round(sym)}" if sym is not None else "Análisis facial"


@app.get("/story/{stem}", response_class=HTMLResponse)
def story_page(stem: str, card: int = -1):
    """Tarjetas 9:16 para compartir. ?card=n muestra solo una a 1080×1920 (para capturar PNG)."""
    from .ui import head, STORY_CSS, STORY_JS
    stem = Path(stem).name
    one = card >= 0
    css = STORY_CSS + (".stack{display:flex;flex-direction:column;gap:40px;align-items:center;padding:40px}.stack .story{transform:scale(.5);transform-origin:top center;margin-bottom:-960px}" if not one else "html,body{margin:0;width:1080px;height:1920px;overflow:hidden}")
    pick = ("c[%d]||c[0]" % card) if one else "c.join('')"
    body = ('<body><div id="st" class="%s"></div><script>%s\nfetch(\'/api/report/%s\').then(r=>r.json()).then(R=>{const c=storyCards(R);document.getElementById(\'st\').innerHTML=%s;document.body.dataset.ready=\'1\'});</script></body></html>'
            % ("" if one else "stack", STORY_JS, stem, pick))
    return head("Para compartir · facelab", css) + body


@app.get("/api/card/{stem}/{n}")
async def story_card_png(stem: str, n: int):
    """Captura la tarjeta n con Chrome headless a 1080×1920 y devuelve el PNG."""
    import anyio
    stem = Path(stem).name
    if not (OUT_DIR / f"{stem}.json").exists():
        return JSONResponse({"error": "informe no encontrado"}, status_code=404)
    chrome = _find_chrome()
    if not chrome:
        return JSONResponse({"error": "no se encontró Chrome para capturar la tarjeta"}, status_code=500)
    png = OUT_DIR / f"{stem}_card_{n}.png"
    port = int(os.environ.get("FACELAB_PORT", "8766"))
    cmd = [chrome, "--headless=new", "--disable-gpu", "--no-sandbox", "--hide-scrollbars", "--run-all-compositor-stages-before-draw", "--virtual-time-budget=8000",
           "--window-size=1080,1920", f"--screenshot={png}", f"--user-data-dir={OUT_DIR / '.chrome-pdf'}", f"http://127.0.0.1:{port}/story/{stem}?card={n}"]
    size = await anyio.to_thread.run_sync(lambda: _chrome_capture(cmd, png, 20_000))
    if not png.exists() or size < 20_000:
        return JSONResponse({"error": "Chrome no produjo la tarjeta a tiempo"}, status_code=500)
    return FileResponse(png, media_type="image/png", filename=f"facelab-{stem}-{n}.png")


@app.post("/analyze")
async def analyze_upload(file: UploadFile = File(...), sex: str = Form(""), ancestry: str = Form(""), age: str = Form(""), full: str = Form("1"),
                         person: str = Form(""), profile_photo: UploadFile | None = File(None), ambition: str = Form(""), feed: str = Form("1")):
    """Guarda la foto, lanza el informe completo en segundo plano y devuelve el stem para redirigir."""
    from .pipeline import start_background
    IN_DIR.mkdir(parents=True, exist_ok=True); OUT_DIR.mkdir(parents=True, exist_ok=True)
    stem = re.sub(r"[^A-Za-z0-9_-]", "_", Path(file.filename or "foto").stem) + f"_{int(time.time())}"
    ext = Path(file.filename or "foto.jpg").suffix.lower() or ".jpg"
    src = IN_DIR / f"{stem}{ext}"
    src.write_bytes(await file.read())
    out_json = OUT_DIR / f"{stem}.json"
    prof = Profile(sex=sex or None, ancestry=ancestry or None, age=int(age) if age.isdigit() else None, ambition=ambition or None)
    steps = None if full == "1" else {"analysis", "visual"}
    prof_src = None
    if profile_photo is not None and profile_photo.filename:
        pext = Path(profile_photo.filename).suffix.lower() or ".jpg"
        prof_src = IN_DIR / f"{stem}_profile{pext}"; prof_src.write_bytes(await profile_photo.read())
    meta = {"src": str(src), "profile": prof.to_dict(), "person": person.strip(), "profile_src": str(prof_src) if prof_src else None, "date": time.strftime("%Y-%m-%d %H:%M"), "feed": feed != "0"}
    (OUT_DIR / f"{stem}.meta.json").write_text(json.dumps(meta))
    start_background(src, out_json, prof, steps, meta=meta)
    return {"stem": stem, "report_url": f"/report/{stem}"}


@app.get("/api/status/{stem}")
def status(stem: str):
    p = OUT_DIR / f"{Path(stem).name}.status.json"
    if not p.exists():
        return JSONResponse({"error": "sin estado"}, status_code=404)
    return json.loads(p.read_text())


@app.post("/api/regen/{stem}")
async def regen(stem: str, body: dict):
    """Vuelve a ejecutar pasos concretos: {"steps": ["narrative","protocol","visualize"]}"""
    from .pipeline import start_background
    stem = Path(stem).name
    out_json, meta = OUT_DIR / f"{stem}.json", OUT_DIR / f"{stem}.meta.json"
    if not out_json.exists():
        return JSONResponse({"error": "informe no encontrado"}, status_code=404)
    report = json.loads(out_json.read_text())
    m = json.loads(meta.read_text()) if meta.exists() else {"src": report.get("source"), "profile": report.get("profile", {})}
    steps = set(body.get("steps") or ["narrative", "protocol", "visualize"])
    if body.get("look_ids"):
        m["look_ids"] = list(body["look_ids"])
    prof_d = dict(m.get("profile") or {})
    if body.get("ambition"):
        prof_d["ambition"] = body["ambition"]; m["profile"] = prof_d; meta.write_text(json.dumps(m))
        report["profile"] = {**(report.get("profile") or {}), "ambition": body["ambition"]}
    start_background(Path(m["src"]), out_json, Profile(**{k: v for k, v in prof_d.items() if k in ("sex", "ancestry", "age", "ambition")}), steps, report, meta=m)
    return {"ok": True, "steps": sorted(steps)}


@app.post("/narrate")
async def narrate_report(body: dict):
    from .narrate import narrate_async
    p = Path(body.get("json_path", ""))
    if not p.exists() or p.parent != OUT_DIR:
        return JSONResponse({"error": "informe no encontrado"}, status_code=404)
    report = json.loads(p.read_text())
    try:
        report["narrative"] = await narrate_async(report)
    except Exception as e:
        return JSONResponse({"error": f"fallo al redactar: {e}"}, status_code=500)
    p.write_text(json.dumps(report, indent=2, ensure_ascii=False))
    return {"narrative": report["narrative"]}


@app.post("/protocol")
async def protocol_report(body: dict):
    from .protocol import build_async
    p = Path(body.get("json_path", ""))
    if not p.exists() or p.parent != OUT_DIR:
        return JSONResponse({"error": "informe no encontrado"}, status_code=404)
    report = json.loads(p.read_text())
    try:
        report["protocol"] = await build_async(report)
    except Exception as e:
        return JSONResponse({"error": f"fallo al generar el protocolo: {e}"}, status_code=500)
    p.write_text(json.dumps(report, indent=2, ensure_ascii=False))
    return {"protocol": report["protocol"]}


@app.post("/visualize")
async def visualize_report(body: dict):
    from .visualize import generate
    import anyio
    p = Path(body.get("json_path", ""))
    if not p.exists() or p.parent != OUT_DIR:
        return JSONResponse({"error": "informe no encontrado"}, status_code=404)
    report = json.loads(p.read_text())
    try:
        report["visualization"] = await anyio.to_thread.run_sync(lambda: generate(report, OUT_DIR, p.stem))
    except Exception as e:
        return JSONResponse({"error": f"fallo al visualizar: {e}"}, status_code=500)
    p.write_text(json.dumps(report, indent=2, ensure_ascii=False))
    return {"visualization": report["visualization"]}


@app.get("/report/{stem}", response_class=HTMLResponse)
def report_page(stem: str):
    from .report_page import PAGE as REPORT
    return REPORT


@app.get("/api/report/{stem}")
def report_json(stem: str):
    p = OUT_DIR / f"{Path(stem).name}.json"
    if not p.exists():
        return JSONResponse({"error": "no existe"}, status_code=404)
    try:
        d = json.loads(p.read_text(), parse_constant=lambda c: None)
    except json.JSONDecodeError:
        return JSONResponse({"error": "escribiendo"}, status_code=409)
    d = _sanitize(d)
    d["catalog"] = {k: {"name": v["name"], "norm": v.get("norm"), "unit": v.get("unit")} for k, v in CATALOG_BY_ID.items()}
    d["stem"] = p.stem
    d["json_path"] = str(p)
    return d


@app.get("/reports")
def list_reports():
    items = []
    for p in sorted(OUT_DIR.glob("*.json"), key=lambda x: x.stat().st_mtime, reverse=True):
        if p.name.endswith((".status.json", ".meta.json")):
            continue
        try:
            d = json.loads(p.read_text())
        except json.JSONDecodeError:
            continue
        sc = d.get("scores", {})
        items.append({"stem": p.stem, "profile": d.get("profile"), "face": d.get("assets", {}).get("face"), "has_narrative": "narrative" in d, "has_protocol": "protocol" in d,
                      "person": d.get("person"), "date": d.get("date"), "review": d.get("review"),
                      "scores": {"simetría": (sc.get("symmetry") or {}).get("score"), "averageness": (sc.get("averageness") or {}).get("score"), "proporcionalidad": (sc.get("proportionality") or {}).get("score"), "edad visual": (d.get("age") or {}).get("visual_age")}})
    return items


@app.get("/admin", response_class=HTMLResponse)
@app.get("/admin/{stem}", response_class=HTMLResponse)
def admin_page(stem: str = ""):
    from .admin_page import ADMIN
    return ADMIN


@app.get("/people", response_class=HTMLResponse)
@app.get("/compare", response_class=HTMLResponse)
def people_page():
    from .admin_page import PEOPLE
    return PEOPLE


@app.put("/api/review/{stem}")
async def review_put(stem: str, body: dict):
    """Guarda ediciones humanas de narrativa/protocolo y el estado de revisión."""
    p = OUT_DIR / f"{Path(stem).name}.json"
    if not p.exists():
        return JSONResponse({"error": "informe no encontrado"}, status_code=404)
    d = json.loads(p.read_text())
    for k in ("narrative", "protocol"):
        if isinstance(body.get(k), dict):
            d[k] = body[k]
    if isinstance(body.get("review"), dict):
        d["review"] = {**d.get("review", {}), **body["review"]}
    tmp = p.with_suffix(".json.tmp"); tmp.write_text(json.dumps(d, indent=2, ensure_ascii=False)); tmp.replace(p)
    return {"ok": True, "review": d.get("review")}


CHROME_CANDIDATES = ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "/Volumes/macexternal/Apps/Google Chrome.app/Contents/MacOS/Google Chrome", "/Applications/Chromium.app/Contents/MacOS/Chromium",
                     "/usr/bin/google-chrome", "/usr/bin/chromium", "/usr/bin/chromium-browser"]


def _find_chrome() -> str | None:
    import shutil, subprocess
    chrome = next((c for c in CHROME_CANDIDATES if Path(c).exists()), None) or shutil.which("google-chrome") or shutil.which("chromium")
    if not chrome:
        try:
            found = subprocess.run(["mdfind", "kMDItemCFBundleIdentifier == 'com.google.Chrome'"], capture_output=True, text=True, timeout=10).stdout.split("\n")[0].strip()
            if found and (Path(found) / "Contents/MacOS/Google Chrome").exists():
                chrome = str(Path(found) / "Contents/MacOS/Google Chrome")
        except Exception:
            pass
    return chrome


def _chrome_capture(cmd: list[str], out: Path, min_size: int) -> int:
    """Chrome deja procesos auxiliares vivos y no sale: esperamos a que el archivo exista y deje de crecer, y matamos el grupo."""
    import signal, subprocess, time as _t
    if out.exists():
        out.unlink()
    proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
    last, stable, t0 = -1, 0, _t.time()
    while _t.time() - t0 < 110:
        _t.sleep(1.0)
        size = out.stat().st_size if out.exists() else -1
        if size > min_size and size == last:
            stable += 1
            if stable >= 2:
                break
        else:
            stable = 0
        last = size
        if proc.poll() is not None and size > min_size:
            break
    try:
        os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
    except Exception:
        pass
    return size


@app.get("/api/pdf/{stem}")
async def report_pdf(stem: str):
    """Imprime el informe a PDF con Chrome headless (modo ?print=1) y lo devuelve."""
    import anyio
    stem = Path(stem).name
    if not (OUT_DIR / f"{stem}.json").exists():
        return JSONResponse({"error": "informe no encontrado"}, status_code=404)
    chrome = _find_chrome()
    if not chrome:
        return JSONResponse({"error": "no se encontró Chrome para imprimir; usa Imprimir → Guardar como PDF en el navegador"}, status_code=500)
    pdf = OUT_DIR / f"{stem}.pdf"
    port = int(os.environ.get("FACELAB_PORT", "8766"))
    url = f"http://127.0.0.1:{port}/report/{stem}?print=1"
    cmd = [chrome, "--headless=new", "--disable-gpu", "--no-sandbox", "--hide-scrollbars", "--run-all-compositor-stages-before-draw",
           "--virtual-time-budget=25000", "--window-size=1240,1600", "--no-pdf-header-footer", f"--print-to-pdf={pdf}",
           f"--user-data-dir={OUT_DIR / '.chrome-pdf'}", url]
    size = await anyio.to_thread.run_sync(lambda: _chrome_capture(cmd, pdf, 10_000))
    if not pdf.exists() or pdf.stat().st_size < 10_000:
        return JSONResponse({"error": "Chrome no produjo el PDF a tiempo"}, status_code=500)
    return FileResponse(pdf, media_type="application/pdf", filename=f"informe-{stem}.pdf")


@app.get("/out/{name}")
def out_file(name: str):
    return FileResponse(OUT_DIR / Path(name).name)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=int(os.environ.get("FACELAB_PORT", "8766")), log_level="warning")
