"""Portada tipo producto: hero con escaneo, sección IA con panel lavanda, manifiesto con píldoras, transformaciones,
guía, filosofía, planes, FAQ, pie y asistente de onboarding en 5 pasos."""
from .ui import head

CSS = r"""
body{overflow-x:hidden}
body.flat .hero{min-height:0}body.flat .reveal{opacity:1;transform:none}body.flat .words h2 span,body.flat .words h2 span b{color:var(--ink)}body.flat .words h2 span:not(:has(b)){color:#8f8fa0}
/* nav propia de la portada */
header.top nav a.sec{color:var(--muted)}header.top .contact{border:1px solid var(--line);border-radius:999px;padding:8px 14px;font-weight:600;color:var(--ink);text-decoration:none;font-size:13px}
/* hero */
.hero{display:grid;grid-template-columns:minmax(0,4.2fr) minmax(0,5.6fr) minmax(0,2.2fr);gap:24px;align-items:center;min-height:calc(100vh - 62px);padding:24px 0 20px;position:relative}
.hero:before{content:"";position:absolute;inset:-40px -200px 0;background:radial-gradient(60% 55% at 55% 45%,#f4efff 0%,rgba(255,255,255,0) 70%);z-index:-1;pointer-events:none}
.hero .copy p.lede{margin:0 0 28px;font-size:16px}.hero .cta{display:flex;gap:10px;flex-wrap:wrap;align-items:center}
.hero h1{font-size:clamp(40px,4.6vw,68px);max-width:12ch}
.stage{position:relative;aspect-ratio:1;width:100%;max-width:680px;margin:0 auto}
.stage .ph{position:absolute;inset:0;border-radius:44px;overflow:hidden}
.stage .ph img{width:100%;height:100%;object-fit:cover;display:block;-webkit-mask-image:radial-gradient(62% 60% at 50% 44%,#000 34%,transparent 72%);mask-image:radial-gradient(62% 60% at 50% 44%,#000 34%,transparent 72%)}
.stage .ph.none{background:radial-gradient(60% 60% at 50% 45%,#efe9ff,#fff 80%)}
.kpis{display:flex;flex-direction:column;gap:30px;justify-content:center}.kpi{display:flex;gap:14px;align-items:center}
.kpi .ic{width:46px;height:46px;border-radius:14px;background:var(--panel);display:flex;align-items:center;justify-content:center;flex:none}.kpi .ic svg{width:22px;height:22px;stroke:var(--accent);fill:none;stroke-width:1.5;stroke-linecap:round;stroke-linejoin:round}
.kpi .big{font-size:34px}.kpi .big small{font-size:12px;margin-top:4px}
.trust{display:inline-flex;align-items:center;gap:10px;margin-bottom:24px}
@media(max-width:1000px){.hero{grid-template-columns:1fr;min-height:0;gap:30px}.kpis{flex-direction:row;flex-wrap:wrap;gap:18px}.kpi{flex:1 1 140px}}
/* sección IA: foto + panel lavanda */
.ai{display:grid;grid-template-columns:minmax(0,1.05fr) minmax(0,1fr);border-radius:40px;overflow:hidden;min-height:620px;margin-top:110px;box-shadow:0 30px 80px rgba(17,17,20,.08)}
.ai .pic{position:relative;background:var(--panel);min-height:420px}.ai .pic img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.ai .lbl{position:absolute;display:flex;align-items:center;gap:10px;color:#fff;font-size:11px;letter-spacing:.14em;text-transform:uppercase;font-weight:600;text-shadow:0 1px 8px rgba(0,0,0,.5)}.ai .lbl i{width:8px;height:8px;border-radius:50%;background:#fff;box-shadow:0 0 0 4px rgba(255,255,255,.25)}
.ai .panel{background:linear-gradient(180deg,#ece4ff 0%,#f7f4ff 45%,#fff 100%);display:flex;flex-direction:column;align-items:center;text-align:center;padding:90px 60px 60px}
.ai .panel h2{font-size:clamp(30px,3.4vw,44px)}.ai .panel p{max-width:42ch;color:#55556a;font-size:15px;margin:10px 0 0}
.ai .arrow{margin-top:auto;height:150px;width:2px;background:linear-gradient(180deg,rgba(109,76,255,0),var(--accent3));position:relative}.ai .arrow:after{content:"";position:absolute;bottom:-2px;left:-5px;width:10px;height:10px;border-right:2px solid var(--accent3);border-bottom:2px solid var(--accent3);transform:rotate(45deg)}
@media(max-width:900px){.ai{grid-template-columns:1fr}.ai .panel{padding:50px 26px}}
/* manifiesto */
.words{text-align:center;padding:170px 0 150px;position:relative}.words h2{font-size:clamp(30px,4.2vw,58px);font-weight:300;max-width:24ch;margin:0 auto;line-height:1.08;letter-spacing:-.03em}
.words h2 span{color:#c9c9d4;transition:color .5s}.words h2 span.on{color:#8f8fa0}.words h2 span.on b{color:var(--ink)}.words h2 b{font-weight:600;color:#c9c9d4;transition:color .5s}
.words .float{position:absolute}
/* transformaciones */
.tr{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px;margin-top:30px}@media(max-width:900px){.tr{grid-template-columns:1fr}}
.cmp{position:relative;aspect-ratio:4/5;border-radius:28px;overflow:hidden;background:var(--panel);box-shadow:0 14px 40px rgba(17,17,20,.08)}.cmp img{width:100%;height:100%;object-fit:cover;display:block}
.cmp .after{position:absolute;inset:0;background-size:cover;background-position:center;clip-path:inset(0 0 0 50%)}.cmp input{position:absolute;inset:0;width:100%;height:100%;margin:0;opacity:0;cursor:ew-resize}
.cmp .lbl{position:absolute;bottom:14px;font-size:10px;letter-spacing:.12em;text-transform:uppercase;font-weight:700;background:rgba(17,17,20,.7);color:#fff;padding:5px 10px;border-radius:999px;pointer-events:none}.cmp .lbl.l{left:14px}.cmp .lbl.r{right:14px}
.cmp .mid{position:absolute;top:0;bottom:0;width:2px;background:#fff;left:50%;pointer-events:none;box-shadow:0 0 0 1px rgba(0,0,0,.15)}.cmp .mid:after{content:"⇔";position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:34px;height:34px;border-radius:50%;background:#fff;color:var(--ink);display:flex;align-items:center;justify-content:center;font-size:14px;box-shadow:0 4px 14px rgba(0,0,0,.18)}
.tr .who{display:flex;justify-content:space-between;align-items:center;margin-top:10px;font-size:13px}.tr .who b{font-weight:600}
/* guía: rejilla de funciones */
.feat{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px;margin-top:30px}@media(max-width:900px){.feat{grid-template-columns:1fr}}
.feat .card{padding:24px;border-radius:26px;min-height:200px;display:flex;flex-direction:column}.feat .card .ic{width:40px;height:40px;border-radius:12px;background:var(--accent2);display:flex;align-items:center;justify-content:center;margin-bottom:16px}.feat .card .ic svg{width:20px;height:20px;stroke:var(--accent);fill:none;stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round}
.feat h3{font-size:18px;letter-spacing:-.02em;margin:0 0 6px}.feat p{margin:0;color:var(--muted);font-size:14px}.feat .src{margin-top:auto;padding-top:14px;font-size:11px;color:var(--accent);font-weight:600}
/* filosofía */
.phil{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.2fr);gap:50px;align-items:start;margin-top:30px}@media(max-width:900px){.phil{grid-template-columns:1fr}}
.phil ol{list-style:none;margin:0;padding:0;counter-reset:p}.phil li{counter-increment:p;padding:22px 0;border-top:1px solid var(--line);display:grid;grid-template-columns:52px 1fr;grid-template-areas:'n t' 'n p';column-gap:12px}.phil li:before{grid-area:n}.phil li b{grid-area:t}.phil li p{grid-area:p}.phil li:before{content:"0" counter(p);font-weight:700;color:var(--accent);font-size:13px;letter-spacing:.1em;margin-top:4px}.phil li b{display:block;font-size:17px;letter-spacing:-.02em;margin-bottom:4px}.phil li p{margin:0;color:var(--muted);font-size:14px}
/* planes */
.plans{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px;margin-top:30px}@media(max-width:900px){.plans{grid-template-columns:1fr}}
.plan{border:1px solid var(--line);border-radius:28px;padding:28px;display:flex;flex-direction:column;background:#fff}.plan.hi{background:var(--ink);color:#fff;border-color:var(--ink)}.plan .nm{font-size:12px;letter-spacing:.14em;text-transform:uppercase;font-weight:700;color:var(--accent)}.plan.hi .nm{color:var(--accent3)}
.plan .pr{font-size:40px;font-weight:800;letter-spacing:-.04em;margin:10px 0 2px}.plan .pr small{font-size:13px;font-weight:500;letter-spacing:0;opacity:.7}.plan p{margin:0 0 16px;font-size:14px;opacity:.8}.plan ul{list-style:none;margin:0 0 22px;padding:0;font-size:14px}.plan li{padding:7px 0;border-top:1px solid rgba(128,128,150,.18);display:flex;gap:10px}.plan li:before{content:"✓";color:var(--accent);font-weight:800}.plan.hi li:before{color:var(--accent3)}.plan .btn{margin-top:auto;justify-content:center}
/* faq */
.faq{max-width:760px;margin-top:22px}.faq details{border-top:1px solid var(--line);padding:16px 0}.faq summary{cursor:pointer;font-weight:600;font-size:16px;list-style:none;display:flex;justify-content:space-between;align-items:center}.faq summary:after{content:"+";font-weight:400;color:var(--muted);font-size:20px}.faq details[open] summary:after{content:"–"}.faq p{margin:10px 0 0;color:var(--muted);font-size:14px;max-width:62ch}
/* cta final y pie */
.final{margin-top:130px;border-radius:40px;background:radial-gradient(80% 120% at 50% 0%,#efe9ff,#fff 70%);text-align:center;padding:90px 30px}.final h2{font-size:clamp(34px,5vw,66px)}
footer.big{margin-top:90px;border-top:1px solid var(--line);padding:40px 0 30px;display:grid;grid-template-columns:2fr 1fr 1fr 1fr;gap:30px;font-size:13px;color:var(--muted)}footer.big b{display:block;color:var(--ink);margin-bottom:10px}footer.big a{display:block;text-decoration:none;color:var(--muted);margin-bottom:6px}footer.big a:hover{color:var(--ink)}
@media(max-width:900px){footer.big{grid-template-columns:1fr 1fr}}
section{padding:110px 0 0}.sec-head{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:30px;align-items:end}@media(max-width:900px){.sec-head{grid-template-columns:1fr}}
.reveal{opacity:0;transform:translateY(18px);transition:.7s cubic-bezier(.2,.7,.2,1)}.reveal.in{opacity:1;transform:none}
/* onboarding */
#ob{position:fixed;inset:0;z-index:50;background:rgba(17,17,20,.45);backdrop-filter:blur(8px);display:none;align-items:center;justify-content:center;padding:20px}#ob.open{display:flex}
.obw{background:#fff;border-radius:30px;width:min(720px,100%);max-height:calc(100vh - 40px);overflow:auto;padding:34px 36px;box-shadow:0 40px 100px rgba(17,17,20,.25);position:relative}
.dots{display:flex;gap:6px;margin-bottom:18px}.dots i{height:6px;flex:1;border-radius:99px;background:var(--panel2)}.dots i.on{background:var(--accent)}
.obw h2{font-size:32px;margin:0 0 8px}.obw .lede{font-size:16px;margin:0 0 22px}
.opts{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px}.opt{border:1.5px solid var(--line);border-radius:18px;padding:14px;cursor:pointer;transition:.12s}.opt:hover{border-color:var(--accent3)}.opt.on{border-color:var(--accent);background:var(--accent2)}.opt b{display:block;font-size:15px}.opt small{color:var(--muted);font-size:12px;display:block;margin-top:3px}
.field{margin:14px 0}.field label{display:block;font-size:12px;font-weight:600;color:var(--muted);margin-bottom:6px;letter-spacing:.04em;text-transform:uppercase}
.field input[type=text],.field input[type=number]{font:15px var(--font);padding:12px 14px;border:1.5px solid var(--line);border-radius:14px;width:100%;background:#fff}.field input:focus{outline:none;border-color:var(--accent)}
.chips{display:flex;flex-wrap:wrap;gap:8px}.chips .opt{padding:9px 14px;border-radius:999px}
.drop{border:2px dashed var(--accent3);border-radius:22px;padding:26px;text-align:center;background:var(--panel);cursor:pointer;position:relative;min-height:190px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:6px}.drop.over{background:var(--accent2)}.drop img{max-height:220px;border-radius:14px}
.check{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:14px;font-size:13px}.check div{display:flex;gap:8px;align-items:flex-start;color:var(--muted)}.check div:before{content:"✓";color:var(--accent);font-weight:800}
.obnav{display:flex;justify-content:space-between;align-items:center;margin-top:26px;gap:10px}
.close{position:absolute;top:16px;right:18px;border:0;background:var(--panel);width:34px;height:34px;border-radius:50%;font-size:16px;cursor:pointer}
.sw{display:flex;align-items:center;gap:10px;margin-top:14px;font-size:14px}.sw input{width:42px;height:24px;appearance:none;background:var(--panel2);border-radius:99px;position:relative;cursor:pointer}.sw input:checked{background:var(--accent)}.sw input:before{content:"";position:absolute;top:3px;left:3px;width:18px;height:18px;border-radius:50%;background:#fff;transition:.15s}.sw input:checked:before{left:21px}
.err{background:#fbe3e0;color:var(--red);border-radius:12px;padding:10px 14px;font-size:13px;margin-top:12px}
"""

ICONS = {
    "scan": '<svg viewBox="0 0 24 24"><path d="M4 8V6a2 2 0 0 1 2-2h2M16 4h2a2 2 0 0 1 2 2v2M20 16v2a2 2 0 0 1-2 2h-2M8 20H6a2 2 0 0 1-2-2v-2"/><circle cx="12" cy="12" r="3.5"/></svg>',
    "layers": '<svg viewBox="0 0 24 24"><path d="m12 3 9 5-9 5-9-5 9-5Z"/><path d="m3 13 9 5 9-5"/></svg>',
    "palette": '<svg viewBox="0 0 24 24"><path d="M12 3a9 9 0 1 0 0 18c1.5 0 2-1 2-2s-1-2 0-3 3 0 4-1 1-3 1-4a9 9 0 0 0-7-8Z"/><circle cx="8" cy="10" r="1"/><circle cx="12" cy="7" r="1"/><circle cx="16" cy="10" r="1"/></svg>',
    "sparkle": '<svg viewBox="0 0 24 24"><path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.5 2.5M15.5 15.5 18 18M6 18l2.5-2.5M15.5 8.5 18 6"/></svg>',
    "face": '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M8 10h.01M16 10h.01M8.5 15a4.5 4.5 0 0 0 7 0"/></svg>',
    "drop": '<svg viewBox="0 0 24 24"><path d="M12 3s6 6.5 6 11a6 6 0 0 1-12 0c0-4.5 6-11 6-11Z"/></svg>',
    "plan": '<svg viewBox="0 0 24 24"><path d="M9 6h11M9 12h11M9 18h11M4 6h.01M4 12h.01M4 18h.01"/></svg>',
    "shirt": '<svg viewBox="0 0 24 24"><path d="m8 4 4 2 4-2 4 4-3 2v11H7V10L4 8l4-4Z"/></svg>',
    "profile": '<svg viewBox="0 0 24 24"><path d="M14 4c-3 0-6 3-6 8s3 8 6 8M14 4h2M14 20h2M8 12h4"/></svg>',
}


def _nav() -> str:
    links = "".join(f'<a class="sec" href="#{h}">{l}</a>' for h, l in (("explorar", "Explorar"), ("tu-cara", "Tu cara"), ("transformaciones", "Transformaciones"), ("guia", "Guía IA"), ("filosofia", "Filosofía")))
    return ('<header class="top"><div class="in"><a class="logo" href="/"><i></i>facelab</a>'
            f'<nav>{links}<a href="/feed" class="sec">Feed</a><a class="contact" href="#contacto">Contacto</a><a class="btn dark sm" href="#analizar" onclick="openOb();return false">Analizar mi cara</a></nav></div></header>')


PAGE = head("facelab · Descubre lo que tu cara ya dice de ti", CSS) + "<body>" + _nav() + r"""
<div class="wrap">
<div class="hero" id="explorar">
 <div class="copy fade-up">
  <div class="trust"><span class="avs" id="avs"></span><span class="pill" id="trust">Cargando…</span></div>
  <h1>Descubre lo que tu cara <span class="light">ya dice de ti.</span></h1>
  <p class="lede">La IA mide tu rostro, tus colores y tu piel, los compara con personas parecidas a ti y te dice qué te favorece. En palabras que cualquiera entiende, con la ciencia a un clic.</p>
  <div class="cta"><a class="btn" href="#analizar" onclick="openOb();return false">Analizar mi cara</a><a class="btn ghost" href="/feed">Ver transformaciones</a></div>
  <p class="cap" style="margin-top:14px">≈ 5 minutos · se procesa en tu ordenador · sin notas de belleza</p>
 </div>
 <div class="stage fade-up" id="stage" style="animation-delay:.15s"><div class="ph none" id="heroPh"><img id="heroImg" alt=""></div>
   <div class="scan" style="left:31%;top:34%;width:13%;height:8%"><b>Cejas · tilt 5°</b></div>
   <div class="scan" style="left:56%;top:50%;width:12%;height:10%"><b>Simetría p91</b></div>
   <div class="scan" style="left:38%;top:66%;width:22%;height:8%"><b>Labios · ratio 1.4</b></div>
   <span class="float" style="left:-2%;top:16%"><i></i>Otoño profundo</span>
   <span class="float" style="right:0;top:24%;animation-delay:1s"><i style="background:#c47a1c"></i>Piel · rojez p38</span>
   <span class="float" style="left:8%;bottom:10%;animation-delay:2s"><i style="background:#1f7a4d"></i>Cara ovalada</span>
 </div>
 <div class="kpis fade-up" style="animation-delay:.3s">
  <div class="kpi"><div class="ic">""" + ICONS["scan"] + r"""</div><div class="big">32<small>medidas faciales<br>con percentil</small></div></div>
  <div class="kpi"><div class="ic">""" + ICONS["layers"] + r"""</div><div class="big">1638<small>caras de referencia<br>de seis ascendencias</small></div></div>
  <div class="kpi"><div class="ic">""" + ICONS["palette"] + r"""</div><div class="big">12<small>estaciones de color<br>y 16 camisas</small></div></div>
  <div class="kpi"><div class="ic">""" + ICONS["sparkle"] + r"""</div><div class="big">13<small>looks y cortes<br>sobre tu foto</small></div></div>
 </div>
</div>

<div class="ai reveal" id="tu-cara">
 <div class="pic"><img id="aiImg" alt=""><span class="lbl" style="left:14%;top:26%"><i></i>Simetría</span><span class="lbl" style="left:22%;top:52%"><i></i>Colorimetría</span><span class="lbl" style="left:40%;top:76%"><i></i>Protocolo</span></div>
 <div class="panel"><h2>Análisis facial<br><span class="light">con IA.</span></h2><p>La IA no promete perfección: observa, mide y explica. Cada análisis lee tu cara tal como es hoy y señala, con datos, qué merece atención y qué juega a tu favor.</p><div class="arrow"></div></div>
</div>

<div class="words" id="manifiesto">
 <span class="float" style="left:12%;top:26%"><i></i>Segura</span><span class="float" style="right:16%;top:20%;animation-delay:.7s"><i style="background:#e0457b"></i>Saludable</span>
 <span class="float" style="left:20%;bottom:22%;animation-delay:1.4s"><i style="background:#1f7a4d"></i>Con luz</span><span class="float" style="right:14%;bottom:30%;animation-delay:2.1s"><i style="background:#c47a1c"></i>Feliz</span>
 <h2 id="wordsH">facelab te ayuda a <b>entender tu cara</b> como nunca: medidas reales, <b>explicadas para cualquiera</b> y respaldadas por <b>ciencia publicada</b>, no por opiniones.</h2>
</div>

<section id="transformaciones">
 <div class="sec-head reveal"><div><div class="eyebrow">Transformaciones</div><h2>Antes y después,<br><span class="light">sin cirugía.</span></h2></div><p class="lede">Proyecciones generadas sobre la foto real de cada persona a partir de su protocolo: piel, cejas, pelo, descanso, ropa. Arrastra para comparar.</p></div>
 <div class="tr reveal" id="tr"></div>
</section>

<section id="guia">
 <div class="sec-head reveal"><div><div class="eyebrow">Guía IA</div><h2>Todo lo que mide,<br><span class="light">y para qué sirve.</span></h2></div><p class="lede">Seis módulos que trabajan sobre la misma foto. Cada uno cita su fuente y devuelve percentiles dentro de tu grupo.</p></div>
 <div class="feat reveal">
  <div class="card"><div class="ic">""" + ICONS["scan"] + r"""</div><h3>Medidas antropométricas</h3><p>478 puntos, 32 proporciones: tercios, quintos, índice facial, tilt cantal, índice nasal, FWHR, mandíbula, simetría.</p><div class="src">Farkas 1994 · Naini 2011</div></div>
  <div class="card"><div class="ic">""" + ICONS["layers"] + r"""</div><h3>Normas de tu grupo</h3><p>Cada medida con su percentil frente a personas de tu mismo sexo y ascendencia. Averageness, dimorfismo y proporcionalidad.</p><div class="src">MEBeauty · Rhodes 2006</div></div>
  <div class="card"><div class="ic">""" + ICONS["drop"] + r"""</div><h3>Piel y edad visual</h3><p>Mapas de rojez, manchas, textura y brillo con percentiles, y una edad visual estimada con su margen de error.</p><div class="src">SegFormer · InsightFace</div></div>
  <div class="card"><div class="ic">""" + ICONS["palette"] + r"""</div><h3>Colorimetría y estilo</h3><p>Estación de color, paleta, forma de cara, la misma foto con 16 camisas, armario, looks y cortes renderizados.</p><div class="src">Jackson 1980 · Russell 2009</div></div>
  <div class="card"><div class="ic">""" + ICONS["plan"] + r"""</div><h3>Protocolo por fases</h3><p>Entre 4 y 16 acciones no quirúrgicas con evidencia, coste, frecuencia y horizonte, secuenciadas hasta 12 meses.</p><div class="src">Biblioteca de 53 métodos</div></div>
  <div class="card"><div class="ic">""" + ICONS["profile"] + r"""</div><h3>Perfil real</h3><p>Con una foto lateral: nasofrontal, nasolabial, mentolabial, convexidad y línea E medidos sobre la silueta real.</p><div class="src">Ricketts · Legan & Burstone</div></div>
 </div>
</section>

<section id="filosofia">
 <div class="phil reveal">
  <div><div class="eyebrow">Filosofía</div><h2>Datos,<br><span class="light">no juicios.</span></h2><p class="lede" style="margin-top:12px">Medimos y explicamos. Nunca decimos si alguien es guapo: decimos qué mide, cómo se compara y qué se puede hacer.</p></div>
  <ol>
   <li><b>Sin notas de belleza</b><p>Cada frase se apoya en un valor, un percentil y una norma citada. Los scores globales se explican con todos sus componentes y sus pesos.</p></li>
   <li><b>Ciencia con fuentes</b><p>Farkas, Naini, Ricketts, Rhodes, Russell, Perrett. Si un dato es orientativo, lo decimos y explicamos por qué.</p></li>
   <li><b>Privado por diseño</b><p>Las fotos y los informes se procesan y se guardan en tu ordenador. Solo el texto redactado por la IA sale a internet.</p></li>
   <li><b>Revisión humana</b><p>Cada informe puede pasar por una cola de revisión donde una persona corrige, aprueba y firma antes de entregarlo.</p></li>
  </ol>
 </div>
</section>

<section id="planes">
 <div class="sec-head reveal"><div><div class="eyebrow">Planes</div><h2>Para ti,<br><span class="light">y para tu equipo.</span></h2></div><p class="lede">El análisis personal es gratuito y local. Los planes de estudio y clínica añaden revisión humana, seguimiento y marca propia.</p></div>
 <div class="plans reveal">
  <div class="plan"><div class="nm">Personal</div><div class="pr">Gratis<small> · en tu ordenador</small></div><p>Informe completo con medidas, colorimetría, protocolo y looks.</p><ul><li>32 medidas con percentil</li><li>Colorimetría y 16 camisas</li><li>Protocolo por fases</li><li>13 looks renderizados</li><li>PDF y tarjetas para compartir</li></ul><a class="btn" href="#analizar" onclick="openOb();return false">Analizar mi cara</a></div>
  <div class="plan hi"><div class="nm">Estudio</div><div class="pr">Próximamente</div><p>Para estilistas, asesores de imagen y centros de estética.</p><ul><li>Cola de revisión y firma</li><li>Seguimiento por persona</li><li>Comparación entre informes</li><li>Feed privado con tu marca</li><li>Exportación en lote</li></ul><a class="btn" href="#contacto" style="background:#fff;color:var(--ink);border-color:#fff">Avísame</a></div>
  <div class="plan"><div class="nm">Clínica</div><div class="pr">A medida</div><p>Integración con tu flujo clínico y normas propias.</p><ul><li>Normas con tu propia población</li><li>Perfil lateral y cefalometría de tejido blando</li><li>Biblioteca de métodos ampliable</li><li>Despliegue en tus equipos</li></ul><a class="btn ghost" href="#contacto">Hablar con nosotros</a></div>
 </div>
</section>

<section id="faq">
 <div class="eyebrow">Preguntas</div><h2>Lo que todo el mundo<br><span class="light">pregunta primero.</span></h2>
 <div class="faq reveal">
  <details open><summary>¿Me va a decir si soy guapo o guapa?</summary><p>No. facelab mide proporciones, colores y piel, y las compara con personas parecidas a ti. Hay una lectura global estadística, pero se muestra con todos sus componentes y con un aviso claro de que es una lectura de una foto, no una nota.</p></details>
  <details><summary>¿Qué foto necesito?</summary><p>Una de frente, con luz de día, sin gafas ni gorro, boca cerrada y sin filtros. Si añades una de perfil a 90°, medimos también los ángulos reales de nariz, labios y mentón.</p></details>
  <details><summary>¿Adónde van mis fotos?</summary><p>Se procesan y se guardan en el ordenador donde corre facelab. Solo el texto de la narrativa y del protocolo pasa por la IA. Puedes elegir no aparecer en el feed.</p></details>
  <details><summary>¿Cuánto tarda?</summary><p>Las medidas salen en segundos. El informe se abre al instante y se completa solo en unos cinco minutos: narrativa, protocolo, proyección y looks.</p></details>
  <details><summary>¿Es un diagnóstico médico?</summary><p>No. Es un análisis geométrico y de color sobre una foto. Cualquier procedimiento o principio activo del protocolo se consulta con un profesional.</p></details>
 </div>
</section>

<div class="final reveal" id="analizar-cta"><div class="eyebrow">Empieza ahora</div><h2>Tu cara, medida<br><span class="light">y explicada.</span></h2><p class="lede" style="margin:10px auto 26px">Cinco minutos. Sin registro. Sin notas de belleza.</p><a class="btn dark" href="#analizar" onclick="openOb();return false">Analizar mi cara</a></div>

<footer class="big" id="contacto">
 <div><span class="logo" style="font-weight:800;font-size:16px;color:var(--ink)">facelab</span><p style="max-width:44ch;margin:10px 0 0">Morfometría facial, colorimetría y estilo sobre una foto, explicados para cualquiera. No presta servicios clínicos ni médicos.</p></div>
 <div><b>Producto</b><a href="#explorar">Explorar</a><a href="#transformaciones">Transformaciones</a><a href="#guia">Guía IA</a><a href="#planes">Planes</a></div>
 <div><b>Herramientas</b><a href="/feed">Feed</a><a href="/people">Personas</a><a href="/admin">Revisión</a><a href="/classic">Subida clásica</a></div>
 <div><b>Contacto</b><a href="mailto:hola@facelab.local">hola@facelab.local</a><a href="https://github.com" target="_blank" rel="noopener">GitHub</a></div>
</footer>
</div>

<div id="ob" role="dialog" aria-modal="true"><div class="obw"><button class="close" onclick="closeOb()" aria-label="Cerrar">✕</button><div class="dots" id="dots"></div><div id="obBody"></div><div class="obnav"><button class="btn ghost" id="obBack" onclick="obStep(-1)">Atrás</button><span class="cap" id="obHint" style="margin:0"></span><button class="btn dark" id="obNext" onclick="obStep(1)">Siguiente</button></div></div></div>

<script>
if(location.search.includes('flat=1'))document.body.classList.add('flat');
const F={sex:'',ancestry:'',age:'',person:'',ambition:'',feed:true,file:null,pfile:null};let step=0;const N=5;
function openOb(){document.getElementById('ob').classList.add('open');step=0;draw()}function closeOb(){document.getElementById('ob').classList.remove('open')}
function pick(k,v,el){F[k]=v;[...el.parentNode.children].forEach(c=>c.classList.toggle('on',c===el))}
function opt(k,v,b,s){return `<div class="opt ${F[k]===v?'on':''}" onclick="pick('${k}','${v}',this)"><b>${b}</b>${s?'<small>'+s+'</small>':''}</div>`}
const STEPS=[
()=>`<div class="eyebrow">Hola 👋</div><h2>Esto es lo que vamos a hacer</h2><p class="lede">En cinco minutos tendrás un informe completo de tu cara. Sin trucos, sin notas de belleza.</p>
<div class="opts" style="grid-template-columns:1fr"><div class="opt on" style="cursor:default"><b>1 · Medimos</b><small>478 puntos sobre tu foto y 32 proporciones, piel y colores.</small></div><div class="opt on" style="cursor:default"><b>2 · Comparamos</b><small>Con personas de tu mismo sexo y ascendencia. Cada dato con su percentil.</small></div><div class="opt on" style="cursor:default"><b>3 · Te lo explicamos</b><small>Qué juega a tu favor, qué colores y cortes te van, un plan y cómo te verías.</small></div></div>`,
()=>`<div class="eyebrow">Paso 1 de 4</div><h2>Cuéntanos de ti</h2><p class="lede">Solo para compararte con gente parecida a ti. Puedes dejar cualquier campo en blanco.</p>
<div class="field"><label>Nombre o apodo</label><input type="text" placeholder="Cómo quieres aparecer en tu informe" value="${F.person}" oninput="F.person=this.value"></div>
<div class="field"><label>Sexo</label><div class="opts">${opt('sex','male','Hombre')}${opt('sex','female','Mujer')}${opt('sex','','Prefiero no decirlo','usa normas de todo el grupo')}</div></div>
<div class="field"><label>Ascendencia (grupo de referencia)</label><div class="chips">${[['hispanic','Hispana / latina'],['caucasian','Caucásica'],['asian','Asiática'],['black','Negra'],['indian','India'],['mideastern','Medio Oriente'],['other','Mixta / otra']].map(([v,l])=>opt('ancestry',v,l)).join('')}</div></div>
<div class="field" style="max-width:160px"><label>Edad</label><input type="number" min="10" max="99" placeholder="años" value="${F.age}" oninput="F.age=this.value"></div>`,
()=>`<div class="eyebrow">Paso 2 de 4</div><h2>Tu foto de frente</h2><p class="lede">La mejor foto es la más aburrida: luz de día, cara relajada, mirando a cámara.</p>
<div class="drop" id="drop" onclick="document.getElementById('f').click()">${F.file?'<img id="prev">':'<b>Arrastra tu foto aquí o toca para elegirla</b><span class="cap" style="margin:0">JPG o PNG · se queda en este ordenador</span>'}<input id="f" type="file" accept="image/*" hidden></div>
<div class="check"><div>Luz natural, sin sombras duras</div><div>Sin gafas ni gorro</div><div>Boca cerrada, sin sonreír</div><div>Sin filtros ni retoques</div></div>
<div class="field" style="margin-top:18px"><label>Foto de perfil (opcional, de lado, 90°)</label><input id="pf" type="file" accept="image/*" style="font:13px var(--font)"><span class="cap">Con ella medimos los ángulos reales de nariz, labios y mentón.</span></div>`,
()=>`<div class="eyebrow">Paso 3 de 4</div><h2>¿Cuánto quieres cambiar?</h2><p class="lede">El plan se adapta a tu ambición. Nunca proponemos cirugía.</p>
<div class="opts">${opt('ambition','','Que decida el análisis','según lo que encuentre')}${opt('ambition','mejora','Mejorar','7–10 acciones, 6 meses')}${opt('ambition','glow-up','Glow-up','11–16 acciones, 12 meses, pelo, barba o cejas, cuerpo, dientes, ropa')}</div>`,
()=>`<div class="eyebrow">Paso 4 de 4</div><h2>Privacidad y listo</h2><p class="lede">Tu foto y tu informe se procesan y se guardan en este ordenador. Nada sale a internet salvo el texto que redacta la IA.</p>
<div class="sw"><input type="checkbox" id="fd" ${F.feed?'checked':''} onchange="F.feed=this.checked"><label for="fd">Mostrar mi resultado en el feed de personas</label></div>
<div class="opts" style="margin-top:18px;grid-template-columns:1fr"><div class="opt on" style="cursor:default"><b>Resumen</b><small>${F.person||'Sin nombre'} · ${({male:'hombre',female:'mujer'})[F.sex]||'sin sexo'} · ${F.ancestry||'sin ascendencia'} · ${F.age?F.age+' años':'sin edad'} · ambición ${F.ambition||'automática'} · ${F.file?F.file.name:'sin foto ⚠'}</small></div></div><div id="oberr"></div>`];
function draw(){document.getElementById('dots').innerHTML=Array.from({length:N},(_,i)=>`<i class="${i<=step?'on':''}"></i>`).join('');document.getElementById('obBody').innerHTML=STEPS[step]();
document.getElementById('obBack').style.visibility=step?'visible':'hidden';const nx=document.getElementById('obNext');nx.textContent=step===0?'Empezar':step===N-1?'Analizar mi cara':'Siguiente';document.getElementById('obHint').textContent=step===2&&!F.file?'Necesitamos la foto para seguir':'';
if(step===2){const f=document.getElementById('f'),d=document.getElementById('drop');f.onchange=()=>setFile(f.files[0]);d.ondragover=e=>{e.preventDefault();d.classList.add('over')};d.ondragleave=()=>d.classList.remove('over');d.ondrop=e=>{e.preventDefault();d.classList.remove('over');setFile(e.dataTransfer.files[0])};
const pf=document.getElementById('pf');pf.onchange=()=>F.pfile=pf.files[0];if(F.file){const r=new FileReader();r.onload=e=>{const p=document.getElementById('prev');if(p)p.src=e.target.result};r.readAsDataURL(F.file)}}}
function setFile(file){if(!file)return;F.file=file;draw()}
async function obStep(d){if(d>0&&step===2&&!F.file){document.getElementById('obHint').textContent='Necesitamos la foto para seguir';return}
if(d>0&&step===N-1){return submit()}step=Math.max(0,Math.min(N-1,step+d));draw()}
async function submit(){const nx=document.getElementById('obNext');nx.disabled=true;nx.textContent='Subiendo…';const fd=new FormData();fd.append('file',F.file);fd.append('sex',F.sex);fd.append('ancestry',F.ancestry);fd.append('age',F.age);fd.append('person',F.person);fd.append('ambition',F.ambition);fd.append('feed',F.feed?'1':'0');if(F.pfile)fd.append('profile_photo',F.pfile);
try{const r=await fetch('/analyze',{method:'POST',body:fd});const j=await r.json();if(j.error)throw new Error(j.error);location.href=j.report_url}catch(e){document.getElementById('oberr').innerHTML='<div class="err">'+e.message+'</div>';nx.disabled=false;nx.textContent='Reintentar'}}
if(location.hash==='#analizar')openOb();window.addEventListener('hashchange',()=>{if(location.hash==='#analizar')openOb()});
/* revelado al hacer scroll */
const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}}),{threshold:.12});document.querySelectorAll('.reveal').forEach(el=>io.observe(el));setTimeout(()=>document.querySelectorAll('.reveal').forEach(el=>el.classList.add('in')),2500);
/* manifiesto: las palabras se encienden al entrar */
const wh=document.getElementById('wordsH');wh.innerHTML=wh.innerHTML.split(/(<b>.*?<\/b>|\s+)/).filter(x=>x&&!/^\s+$/.test(x)).map(w=>`<span>${w}</span>`).join(' ');
const spans=[...wh.querySelectorAll('span')];new IntersectionObserver(es=>{if(es[0].isIntersecting)spans.forEach((s,i)=>setTimeout(()=>s.classList.add('on'),i*45))},{threshold:.4}).observe(wh);setTimeout(()=>spans.forEach(s=>s.classList.add('on')),4000);
/* datos reales del feed */
fetch('/api/feed').then(r=>r.json()).then(l=>{const n=l.length;document.getElementById('trust').textContent=n?`${n} persona${n>1?'s':''} ya se lo ${n>1?'hicieron':'hizo'}`:'Sé la primera persona en analizarse';
document.getElementById('avs').innerHTML=l.slice(0,4).map(x=>x.face?`<img src="/out/${x.face}" alt="">`:`<span>${(x.name||'?')[0]}</span>`).join('');
const h=l.find(x=>x.face);if(h){document.getElementById('heroImg').src='/out/'+h.face;document.getElementById('heroPh').classList.remove('none');document.getElementById('aiImg').src='/out/'+(h.look||h.face)}else{document.getElementById('stage').querySelectorAll('.scan').forEach(s=>s.style.display='none')}
const tr=l.filter(x=>x.after&&x.face).slice(0,3);document.getElementById('tr').innerHTML=tr.length?tr.map((x,i)=>`<div><div class="cmp"><img src="/out/${x.face}" alt="antes"><div class="after" id="a${i}" style="background-image:url('/out/${x.after}')"></div><div class="mid" id="m${i}"></div><input type="range" min="0" max="100" value="50" oninput="document.getElementById('a${i}').style.clipPath='inset(0 0 0 '+this.value+'%)';document.getElementById('m${i}').style.left=this.value+'%'" aria-label="comparar"><span class="lbl l">Antes</span><span class="lbl r">Proyección</span></div><div class="who"><b>${x.name||'Anónimo'}</b><a href="/report/${x.stem}" style="color:var(--accent);text-decoration:none;font-weight:600">Ver informe →</a></div></div>`).join(''):'<p class="cap">Las transformaciones aparecen cuando un informe termina su proyección.</p>'}).catch(()=>{});
</script></body></html>"""
