"""Sistema de diseño compartido: tokens, tipografía, navegación y tarjetas para compartir (stories 9:16).

Estética: blanco aireado, tinta casi negra, acento lavanda, titulares grandes con pesos mezclados, píldoras y cifras grandes con leyenda pequeña.
"""
from __future__ import annotations

FONTS = '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap">'

TOKENS = r""":root{--paper:#ffffff;--panel:#f6f4fb;--panel2:#ebe6f7;--ink:#111114;--muted:#6f6f7c;--line:#e9e7f0;--accent:#6d4cff;--accent2:#efe9ff;--accent3:#c9b8ff;--amber:#c47a1c;--amber2:#fbf0dc;--red:#c2453a;--r:18px;--font:Inter,-apple-system,system-ui,"Segoe UI",sans-serif}
*{box-sizing:border-box}html{scroll-behavior:smooth;-webkit-font-smoothing:antialiased}
body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--font);font-size:15px;line-height:1.55}
.mono{font-family:"JetBrains Mono",ui-monospace,Menlo,monospace}
a{color:inherit}
.wrap{max-width:1240px;margin:0 auto;padding:0 28px 120px}
/* navegación */
header.top{position:sticky;top:0;z-index:20;background:rgba(255,255,255,.82);backdrop-filter:blur(14px);border-bottom:1px solid var(--line)}
header.top .in{max-width:1240px;margin:0 auto;padding:12px 28px;display:flex;align-items:center;gap:14px;font-size:13px;flex-wrap:wrap}
header.top .logo{display:inline-flex;align-items:center;gap:8px;font-weight:800;letter-spacing:-.02em;text-decoration:none;font-size:16px}
header.top .logo i{width:22px;height:22px;border-radius:7px;background:conic-gradient(from 200deg,var(--accent),var(--accent3),#ffd6e8,var(--accent));display:inline-block}
header.top nav{display:flex;gap:18px;margin-left:auto;flex-wrap:wrap;align-items:center}header.top nav a{color:var(--muted);text-decoration:none;font-weight:500}header.top nav a:hover,header.top nav a.on{color:var(--ink)}
.btn{display:inline-flex;align-items:center;gap:8px;font:600 14px var(--font);padding:11px 18px;border-radius:999px;border:1px solid var(--accent2);background:var(--accent2);color:var(--accent);cursor:pointer;text-decoration:none;transition:.15s}
.btn:hover{background:#e6ddff}.btn.dark{background:var(--ink);border-color:var(--ink);color:#fff}.btn.dark:hover{background:#2a2a30}.btn.ghost{background:#fff;border-color:var(--line);color:var(--ink)}.btn.sm{padding:7px 12px;font-size:13px}
.btn[disabled]{opacity:.5;cursor:default}
.pill{display:inline-flex;align-items:center;gap:6px;font-size:12px;padding:5px 12px;border:1px solid var(--line);border-radius:999px;background:#fff;color:var(--muted);box-shadow:0 1px 2px rgba(17,17,20,.04)}
.pill.ok{border-color:#cfe8d8;color:#1f7a4d;background:#eefaf3}.pill.warn{border-color:#f2dcb5;color:var(--amber);background:var(--amber2)}.pill.acc{border-color:var(--accent3);color:var(--accent);background:var(--accent2)}
.pill i{width:8px;height:8px;border-radius:50%;background:currentColor;display:inline-block}
/* tipografía */
h1{font-size:clamp(38px,6vw,72px);line-height:.98;letter-spacing:-.04em;font-weight:800;margin:0 0 16px}h1 .light{font-weight:300}
h2{font-size:clamp(26px,3.2vw,38px);letter-spacing:-.03em;font-weight:800;margin:0 0 8px;line-height:1.05}h2 .light{font-weight:300}
h3{font-size:16px;font-weight:700;margin:0 0 8px;letter-spacing:-.01em}
.eyebrow{font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--accent);font-weight:700;margin-bottom:10px}
.lede{font-size:17px;color:var(--muted);max-width:62ch;font-weight:400}
.big{font-size:clamp(28px,3vw,40px);font-weight:700;letter-spacing:-.03em;line-height:1;font-variant-numeric:tabular-nums}.big small{display:block;font-size:12px;color:var(--muted);font-weight:500;letter-spacing:0;margin-top:6px;line-height:1.3}
.card{background:#fff;border:1px solid var(--line);border-radius:var(--r);padding:16px 18px;box-shadow:0 1px 2px rgba(17,17,20,.03)}
.soft{background:linear-gradient(180deg,#f6f2ff 0%,#fff 100%)}
.cap{font-size:12px;color:var(--muted);margin-top:8px}
/* avatares apilados */
.avs{display:inline-flex;align-items:center}.avs img,.avs span{width:26px;height:26px;border-radius:50%;border:2px solid #fff;object-fit:cover;margin-left:-8px;background:var(--panel2);display:inline-flex;align-items:center;justify-content:center;font-size:10px;font-weight:700;color:var(--accent)}.avs img:first-child,.avs span:first-child{margin-left:0}
/* marcadores de escaneo */
.scan{position:absolute;border:1.5px solid #fff;box-shadow:0 0 0 1px rgba(0,0,0,.15);border-radius:4px}.scan:before{content:"";position:absolute;left:-4px;top:-4px;width:6px;height:6px;border-radius:50%;background:#fff;box-shadow:0 0 0 1px rgba(0,0,0,.2)}
.scan b{position:absolute;left:0;bottom:-20px;font-size:10px;font-weight:600;color:#fff;background:rgba(17,17,20,.7);padding:2px 6px;border-radius:4px;white-space:nowrap;letter-spacing:.02em}
.float{position:absolute;background:#fff;border:1px solid var(--line);border-radius:999px;padding:6px 12px;font-size:12px;font-weight:600;box-shadow:0 8px 24px rgba(17,17,20,.08);display:inline-flex;gap:6px;align-items:center;animation:bob 4s ease-in-out infinite}
.float i{width:8px;height:8px;border-radius:50%;background:var(--accent);display:inline-block}
@keyframes bob{0%,100%{transform:translateY(0)}50%{transform:translateY(-6px)}}
.fade-up{animation:fadeup .7s cubic-bezier(.2,.7,.2,1) both}@keyframes fadeup{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:none}}
@media(prefers-reduced-motion:reduce){.float,.fade-up{animation:none}}
"""


def nav(active: str = "", extra: str = "") -> str:
    links = [("/", "inicio", "Inicio"), ("/feed", "feed", "Feed"), ("/people", "people", "Personas"), ("/admin", "admin", "Revisión")]
    a = "".join(f'<a href="{h}" class="{"on" if k == active else ""}">{l}</a>' for h, k, l in links)
    return (f'<header class="top"><div class="in"><a class="logo" href="/"><i></i>facelab</a>{extra}'
            f'<nav>{a}<a class="btn dark sm" href="/#analizar">Analizar mi cara</a></nav></div></header>')


def head(title: str, css: str = "") -> str:
    return (f'<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{title}</title>{FONTS}<style>{TOKENS}{css}</style></head>')


# ---------- tarjetas para compartir (9:16, 1080×1920) ----------
# Se renderizan con el mismo JS en el informe (a escala) y en /story/<stem> (a tamaño real para capturar PNG).

STORY_CSS = r"""
.story{width:1080px;height:1920px;position:relative;overflow:hidden;background:#fff;color:var(--ink);font-family:var(--font);border-radius:0}
.story .bg{position:absolute;inset:0;background:radial-gradient(120% 70% at 50% 0%,#efe9ff 0%,#fff 60%),#fff}
.story .bg.b2{background:radial-gradient(120% 70% at 50% 100%,#ffe6f1 0%,#fff 60%),#fff}.story .bg.b3{background:radial-gradient(100% 60% at 0% 0%,#e4f3ff 0%,#fff 60%),#fff}
.story .in{position:absolute;inset:0;padding:96px 84px;display:flex;flex-direction:column}
.story .wm{display:flex;align-items:center;gap:14px;font-weight:800;font-size:34px;letter-spacing:-.02em}.story .wm i{width:40px;height:40px;border-radius:12px;background:conic-gradient(from 200deg,#6d4cff,#c9b8ff,#ffd6e8,#6d4cff);display:inline-block}
.story .eb{font-size:22px;letter-spacing:.18em;text-transform:uppercase;color:#6d4cff;font-weight:700;margin:72px 0 18px}
.story h1{font-size:112px;line-height:.96;letter-spacing:-.045em;margin:0 0 28px;font-weight:800}.story h1 .light{font-weight:300}
.story p{font-size:34px;line-height:1.35;color:#4a4a58;margin:0}
.story .face{width:100%;aspect-ratio:1;border-radius:56px;overflow:hidden;background:#f6f4fb;margin-top:40px;box-shadow:0 30px 80px rgba(17,17,20,.12)}.story .face img{width:100%;height:100%;object-fit:cover;display:block}
.story .row{display:flex;gap:18px;flex-wrap:wrap;margin-top:34px}.story .chip{font-size:28px;font-weight:600;padding:16px 28px;border-radius:999px;background:#fff;border:2px solid #e9e7f0;display:inline-flex;align-items:center;gap:14px}
.story .chip i{width:22px;height:22px;border-radius:50%;display:inline-block}
.story .num{font-size:220px;font-weight:800;letter-spacing:-.06em;line-height:.9;margin-top:24px}.story .num small{display:block;font-size:34px;font-weight:500;letter-spacing:0;color:#6f6f7c;margin-top:12px}
.story .sw{display:grid;grid-template-columns:repeat(5,1fr);gap:20px;margin-top:44px}.story .sw div{aspect-ratio:1;border-radius:32px;border:2px solid rgba(0,0,0,.06);position:relative}.story .sw div b{position:absolute;left:0;right:0;bottom:-38px;text-align:center;font-size:20px;font-weight:600;color:#4a4a58}
.story ul{list-style:none;padding:0;margin:36px 0 0}.story li{font-size:40px;line-height:1.25;padding:30px 0;border-top:2px solid #e9e7f0;display:flex;gap:26px;align-items:flex-start}.story li:before{content:"";flex:none;width:22px;height:22px;border-radius:50%;background:#6d4cff;margin-top:18px}
.story .two{display:grid;grid-template-columns:1fr 1fr;gap:24px;margin-top:40px}.story .two div{aspect-ratio:3/4;border-radius:44px;overflow:hidden;background:#f6f4fb;position:relative}.story .two img{width:100%;height:100%;object-fit:cover;display:block}
.story .two b{position:absolute;left:24px;bottom:24px;font-size:26px;font-weight:700;background:rgba(17,17,20,.75);color:#fff;padding:12px 22px;border-radius:999px}
.story .foot{margin-top:auto;display:flex;justify-content:space-between;align-items:flex-end;font-size:24px;color:#6f6f7c}.story .foot b{color:#111114}
"""

STORY_JS = r"""
function storyCards(R){const s=R.scores||{},st=R.style||{},G=(s.global||{}).composite,face=R.assets&&R.assets.face?'/out/'+R.assets.face:'',name=R.person||'Tu cara';
const strengths=[];for(const v of Object.values(R.narrative||{})){(v.strengths||[]).slice(0,1).forEach(x=>strengths.push(x))}
const cards=[];
cards.push(`<div class="story"><div class="bg"></div><div class="in"><div class="wm"><i></i>facelab</div><div class="eb">Análisis facial</div><h1>${name},<br><span class="light">medida y explicada.</span></h1><p>${Object.keys((R.norms||{}).per_measure||{}).length} medidas comparadas con ${R.norms?R.norms.n:0} caras. Sin notas de belleza: datos y explicaciones.</p><div class="face">${face?'<img src="'+face+'">':''}</div><div class="row">${s.symmetry?'<span class="chip">Simetría p'+Math.round(s.symmetry.percentile)+'</span>':''}${st.season?'<span class="chip"><i style="background:'+(st.palette.best[0]||{}).hex+'"></i>'+st.season.name+'</span>':''}${st.face_shape?'<span class="chip">Cara '+st.face_shape.name.toLowerCase()+'</span>':''}</div><div class="foot"><span>Medido con IA · orientativo</span><b>${R.date||''}</b></div></div></div>`);
if(G)cards.push(`<div class="story"><div class="bg b3"></div><div class="in"><div class="wm"><i></i>facelab</div><div class="eb">Lectura global</div><h1>Una cifra,<br><span class="light">con todo lo que la compone.</span></h1><div class="num">${G.score}<small>compuesto 0–100 · averageness, dimorfismo, piel, simetría, proporción, perfil y edad</small></div><div class="row">${Object.entries(G.components||{}).slice(0,6).map(([k,v])=>'<span class="chip">'+({averageness:'Averageness',dimorphism:'Dimorfismo',skin:'Piel',symmetry:'Simetría',proportionality:'Proporción',profile:'Perfil',visual_age:'Edad visual'}[k]||k)+' '+Math.round(typeof v==='object'?(v.score||0):v)+'</span>').join('')}</div><div class="foot"><span>Es una lectura estadística de una foto</span><b>facelab</b></div></div></div>`);
if(st.palette)cards.push(`<div class="story"><div class="bg b2"></div><div class="in"><div class="wm"><i></i>facelab</div><div class="eb">Colorimetría</div><h1>${st.season.name}<br><span class="light">es tu estación.</span></h1><p>${st.season.summary}</p><div class="sw">${st.palette.best.slice(0,10).map(c=>'<div style="background:'+c.hex+'"><b>'+c.name+'</b></div>').join('')}</div><div class="foot" style="margin-top:auto"><span>Metales: ${st.palette.metals}</span><b>Contraste ${st.contrast.level}</b></div></div></div>`);
if(strengths.length)cards.push(`<div class="story"><div class="bg"></div><div class="in"><div class="wm"><i></i>facelab</div><div class="eb">Lo que juega a tu favor</div><h1>Tus puntos<br><span class="light">fuertes.</span></h1><ul>${strengths.slice(0,4).map(x=>'<li>'+x+'</li>').join('')}</ul><div class="foot"><span>Cada frase se apoya en una medida y un percentil</span><b>facelab</b></div></div></div>`);
const V=R.visualization||{};if(V.after&&face)cards.push(`<div class="story"><div class="bg b3"></div><div class="in"><div class="wm"><i></i>facelab</div><div class="eb">Proyección</div><h1>Antes<br><span class="light">y después del protocolo.</span></h1><p>Cambios alcanzables sin cirugía: piel, cejas, pelo, descanso. Nivel ${V.tier||''}.</p><div class="two"><div><img src="${face}"><b>Antes</b></div><div><img src="/out/${V.after}"><b>Después</b></div></div><div class="foot"><span>Ilustración, no promesa</span><b>facelab</b></div></div></div>`);
const rd=st.renders||{},adv=st.advice||{};const look=(adv.outfits||[]).find(o=>rd[o.id]&&rd[o.id].file);if(look)cards.push(`<div class="story"><div class="bg b2"></div><div class="in"><div class="wm"><i></i>facelab</div><div class="eb">Tu look</div><h1>${look.name}<br><span class="light">con tu paleta.</span></h1><div class="two" style="grid-template-columns:1fr"><div style="aspect-ratio:4/5"><img src="/out/${rd[look.id].file}"><b>${look.occasion||''}</b></div></div><div class="foot"><span>${(look.pieces||[]).slice(0,2).join(' · ')}</span><b>facelab</b></div></div></div>`);
return cards}
"""
