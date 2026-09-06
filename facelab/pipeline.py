"""Orquestación del informe completo con estado por pasos (para la UI progresiva).

Estado en out/mine/<stem>.status.json:
{"steps":[{"id","label","state":"pending|running|done|error|skipped","detail"}],"current":id,"done":bool,"error":str|None}
"""
from __future__ import annotations
import json, threading, time, traceback
from pathlib import Path
import cv2
from .profile import Profile

STEPS = [("analysis", "Landmarks y medidas"), ("visual", "Recortes, segmentación, edad y piel"), ("style", "Colorimetría y estilo (Claude)"), ("profile", "Perfil lateral"),
         ("narrative", "Narrativa por sección (Claude)"), ("protocol", "Protocolo (Claude)"), ("visualize", "Visualización (Codex)"), ("looks", "Looks y cortes (Codex)")]


class Status:
    def __init__(self, path: Path):
        self.path = path
        self.data = {"steps": [{"id": i, "label": l, "state": "pending", "detail": ""} for i, l in STEPS], "current": None, "done": False, "error": None, "updated": time.time()}
        self.save()

    @classmethod
    def load(cls, path: Path) -> "Status":
        s = cls.__new__(cls); s.path = path
        s.data = json.loads(path.read_text()) if path.exists() else cls(path).data
        # informes anteriores a un paso nuevo: se añade en su posición con estado pending
        have = {st["id"] for st in s.data["steps"]}
        for i, (sid, label) in enumerate(STEPS):
            if sid not in have:
                s.data["steps"].insert(i, {"id": sid, "label": label, "state": "pending", "detail": ""})
        return s

    def set(self, step: str, state: str, detail: str = ""):
        for st in self.data["steps"]:
            if st["id"] == step:
                st["state"] = state; st["detail"] = detail
        self.data["current"] = step if state == "running" else self.data["current"]
        self.data["updated"] = time.time(); self.save()

    def finish(self, error: str | None = None):
        self.data["done"] = True; self.data["error"] = error; self.data["current"] = None; self.data["updated"] = time.time(); self.save()

    def save(self):
        self.path.write_text(json.dumps(self.data, ensure_ascii=False))


def _save(report: dict, out_json: Path):
    tmp = out_json.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(report, indent=2, ensure_ascii=False)); tmp.replace(out_json)


def run_full(src: Path, out_json: Path, profile: Profile, steps: set[str] | None = None, report: dict | None = None, meta: dict | None = None):
    """Ejecuta los pasos indicados (todos por defecto) y va guardando el JSON y el estado."""
    from .__main__ import build_report, enrich_visual
    from .debug import draw
    steps = steps or {s for s, _ in STEPS}
    status = Status(out_json.with_suffix(".status.json")) if report is None else Status.load(out_json.with_suffix(".status.json"))
    if report is not None:
        status.data["done"] = False; status.data["error"] = None
        for st in status.data["steps"]:
            if st["id"] in steps:
                st["state"] = "pending"
        status.save()
    out_dir, stem = out_json.parent, out_json.stem
    face = None
    try:
        if "analysis" in steps:
            status.set("analysis", "running")
            prev = report or {}
            report, face = build_report(str(src), profile)
            for k in ("assets", "age", "skin", "parsing", "style", "profile_view", "narrative", "protocol", "visualization", "review", "person", "date", "feed"):
                if k in prev and k not in report:
                    report[k] = prev[k]
            if meta:
                report["person"] = meta.get("person") or None; report["date"] = meta.get("date"); report["feed"] = meta.get("feed", True)
            _save(report, out_json); status.set("analysis", "done", f"{len(report.get('norms', {}).get('per_measure', {}))} medidas con percentil")
        if "visual" in steps:
            status.set("visual", "running", "recortes")
            if face is None:
                from .landmarks import detect
                face = detect(str(src))
            enrich_visual(report, face, str(out_json), full=True)
            cv2.imwrite(str(out_dir / f"{stem}_debug.jpg"), draw(face.image_bgr, face.pts))
            from .attractiveness import compute as _global
            report.setdefault("scores", {})["global"] = _global(report)
            _save(report, out_json); status.set("visual", "done", f"edad visual {report.get('age', {}).get('visual_age', '?')} · global {report['scores']['global']['composite']['score']}")
        if "style" in steps:
            status.set("style", "running", "piel, pelo, ojos y paleta")
            try:
                if face is None:
                    from .landmarks import detect
                    face = detect(str(src))
                from .colorimetry import analyze as color_analyze
                prev_style = report.get("style") or {}
                report["style"] = color_analyze(face.image_bgr, face.pts, report, out_dir, stem)
                report["style"]["renders"] = prev_style.get("renders") or {}
                _save(report, out_json)
                status.set("style", "running", f"{report['style']['season']['name']} · asesoría con Claude")
                from .style import advise
                adv = advise(report)
                if adv.get("parse_error"):
                    report["style"]["advice"] = prev_style.get("advice") if prev_style.get("advice") and not prev_style["advice"].get("parse_error") else adv
                    _save(report, out_json); status.set("style", "error", "asesoría inválida" + ("; se conservó la anterior" if prev_style.get("advice") else ""))
                else:
                    report["style"]["advice"] = adv; _save(report, out_json)
                    status.set("style", "done", f"{report['style']['season']['name']} · {len(adv.get('outfits', []))} looks · {len(adv.get('haircuts', []))} cortes")
            except Exception as e:
                status.set("style", "error", str(e)[:200])
        if "profile" in steps:
            psrc = (meta or {}).get("profile_src")
            if psrc and Path(psrc).exists():
                status.set("profile", "running", "silueta y ángulos")
                try:
                    from .profile_view import analyze as profile_analyze
                    report["profile_view"] = profile_analyze(psrc, out_dir, stem, profile.sex)
                    from .attractiveness import compute as _global
                    report.setdefault("scores", {})["global"] = _global(report)
                    _save(report, out_json); status.set("profile", "done", f"{len(report['profile_view']['measures'])} ángulos")
                except Exception as e:
                    status.set("profile", "error", str(e)[:200])
            else:
                status.set("profile", "skipped", "sin foto de perfil")
        if "narrative" in steps:
            status.set("narrative", "running", "6 secciones en paralelo")
            from .narrate import narrate
            new = narrate(report); prev = report.get("narrative") or {}
            failed = [k for k, v in new.items() if v.get("error")]
            merged = {k: (prev[k] if (v.get("error") and k in prev and not prev[k].get("error")) else v) for k, v in new.items()}
            report["narrative"] = merged; _save(report, out_json)
            if failed and len(failed) == len(new):
                status.set("narrative", "error", new[failed[0]]["error"][:160])
            elif failed:
                status.set("narrative", "done", f"{len(failed)} sección(es) con error, se conservó la versión anterior")
            else:
                status.set("narrative", "done")
        if "protocol" in steps:
            status.set("protocol", "running")
            from .protocol import build
            newp = build(report)
            if newp.get("parse_error") and report.get("protocol") and not report["protocol"].get("parse_error"):
                status.set("protocol", "error", "respuesta inválida; se conservó el protocolo anterior")
            else:
                report["protocol"] = newp; _save(report, out_json)
                n_act = sum(len(p.get("actions", [])) for p in newp.get("phases", []))
                status.set("protocol", "error" if newp.get("parse_error") else "done", (newp.get("letter") or "")[:120] if newp.get("parse_error") else f"{n_act} acciones")
        if "visualize" in steps:
            status.set("visualize", "running", "codex image_gen, ~1–2 min")
            try:
                from .visualize import generate
                report["visualization"] = generate(report, out_dir, stem); _save(report, out_json); status.set("visualize", "done")
            except Exception as e:
                status.set("visualize", "error", str(e)[:300])
        if "looks" in steps:
            try:
                from .style import render_looks, render_items
                ids = (meta or {}).get("look_ids") or None
                n = len([i for i in render_items(report) if not ids or i["id"] in set(ids)])
                status.set("looks", "running", f"0/{n} renders con Codex, 3 en paralelo")
                def prog(d, t):
                    _save(report, out_json); status.set("looks", "running", f"{d}/{t} renders con Codex")
                renders = render_looks(report, out_dir, stem, ids, on_progress=prog)
                _save(report, out_json)
                errs = [k for k, v in renders.items() if v.get("error")]
                status.set("looks", "error" if errs and len(errs) == len(renders) else "done", f"{len(renders) - len(errs)} imágenes" + (f", {len(errs)} con error" if errs else ""))
            except Exception as e:
                status.set("looks", "error", str(e)[:300])
        status.finish()
    except Exception as e:
        traceback.print_exc()
        status.set(status.data.get("current") or "analysis", "error", str(e)[:300]); status.finish(error=str(e)[:300])
    return report


def start_background(src: Path, out_json: Path, profile: Profile, steps: set[str] | None = None, report: dict | None = None, meta: dict | None = None) -> threading.Thread:
    t = threading.Thread(target=run_full, args=(src, out_json, profile, steps, report, meta), daemon=True)
    t.start(); return t
