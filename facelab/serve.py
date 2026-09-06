"""API local de facelab (FastAPI). El front vive en web/ (Next.js) y hace proxy a este servidor.

uv run python -m facelab.serve      →  http://127.0.0.1:8766   (API)
cd web && bun run dev               →  http://localhost:3000    (interfaz)
Fotos en samples/mine/, resultados en out/mine/.
"""
from __future__ import annotations
import json, os, re, time
from pathlib import Path
from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse
from .measures import CATALOG_BY_ID
from .profile import Profile

ROOT = Path(__file__).resolve().parent.parent
IN_DIR, OUT_DIR = ROOT / "samples" / "mine", ROOT / "out" / "mine"
WEB_URL = os.environ.get("FACELAB_WEB_URL", "http://127.0.0.1:3000").rstrip("/")  # front Next.js: lo usan el PDF y las tarjetas
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

@app.get("/")
@app.get("/feed")
@app.get("/people")
@app.get("/compare")
@app.get("/admin")
@app.get("/admin/{stem}")
@app.get("/report/{stem}")
@app.get("/story/{stem}")
def web_redirect(request: Request, stem: str = ""):
    """Las páginas viven en el front (web/). Si alguien entra por el puerto de la API, se le redirige."""
    return RedirectResponse(f"{WEB_URL}{request.url.path}" + (f"?{request.url.query}" if request.url.query else ""))


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
    cmd = [chrome, "--headless=new", "--disable-gpu", "--no-sandbox", "--hide-scrollbars", "--run-all-compositor-stages-before-draw", "--virtual-time-budget=8000",
           "--window-size=1080,1920", f"--screenshot={png}", f"--user-data-dir={OUT_DIR / '.chrome-pdf'}", f"{WEB_URL}/story/{stem}?card={n}"]
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
    url = f"{WEB_URL}/report/{stem}?print=1"
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
