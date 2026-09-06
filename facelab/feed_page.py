"""Feed de personas analizadas: tarjetas verticales con scroll a pantalla (móvil) y rejilla (escritorio), con resultados resumidos."""
from .ui import head, nav

CSS = r"""
.top-row{display:flex;align-items:end;justify-content:space-between;gap:16px;flex-wrap:wrap;padding:36px 0 10px}
.tabs{display:flex;gap:6px;background:var(--panel);border-radius:999px;padding:4px}.tabs button{border:0;background:transparent;font:600 13px var(--font);padding:8px 14px;border-radius:999px;cursor:pointer;color:var(--muted)}.tabs button.on{background:#fff;color:var(--ink);box-shadow:0 1px 3px rgba(17,17,20,.08)}
.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px;margin-top:18px}@media(max-width:900px){.grid{grid-template-columns:1fr}}
.fc{position:relative;border-radius:28px;overflow:hidden;background:var(--panel);aspect-ratio:9/16;display:block;text-decoration:none;color:#fff;box-shadow:0 10px 30px rgba(17,17,20,.08)}
.fc img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;display:block}
.fc .top{position:absolute;top:14px;left:14px;right:14px;display:flex;justify-content:space-between;align-items:center;gap:8px}
.fc .who{display:flex;align-items:center;gap:8px;background:rgba(17,17,20,.55);backdrop-filter:blur(8px);padding:6px 12px 6px 6px;border-radius:999px;font-size:13px;font-weight:600}.fc .who span{width:26px;height:26px;border-radius:50%;background:var(--accent);display:inline-flex;align-items:center;justify-content:center;font-size:11px}
.fc .sc{background:#fff;color:var(--ink);font-weight:800;border-radius:999px;padding:6px 12px;font-size:14px;letter-spacing:-.02em}.fc .sc small{font-weight:500;color:var(--muted);margin-left:4px}
.fc .ov{position:absolute;left:0;right:0;bottom:0;padding:18px;background:linear-gradient(transparent,rgba(17,17,20,.9) 70%)}
.fc h3{font-size:22px;letter-spacing:-.03em;margin:0 0 6px;color:#fff}.fc p{margin:0 0 10px;font-size:13px;opacity:.9;line-height:1.4}
.fc .chips{display:flex;gap:6px;flex-wrap:wrap}.fc .chip{font-size:11px;font-weight:600;padding:4px 10px;border-radius:999px;background:rgba(255,255,255,.16);backdrop-filter:blur(6px);display:inline-flex;gap:6px;align-items:center}.fc .chip i{width:9px;height:9px;border-radius:50%;display:inline-block}
.fc .bars{display:flex;gap:10px;margin-top:10px}.fc .bar{flex:1}.fc .bar small{font-size:10px;letter-spacing:.06em;text-transform:uppercase;opacity:.8}.fc .bar b{display:block;font-size:16px}.fc .bar i{display:block;height:4px;border-radius:99px;background:rgba(255,255,255,.25);margin-top:4px;overflow:hidden}.fc .bar i:before{content:"";display:block;height:100%;width:var(--w);background:#fff}
.fc .rev{position:absolute;right:14px;bottom:14px;font-size:10px;font-weight:700;background:#eefaf3;color:#1f7a4d;padding:4px 8px;border-radius:999px}
/* modo historias: una tarjeta por pantalla, scroll con snap */
body.stories .wrap{max-width:none;padding:0}body.stories .top-row,body.stories footer{display:none}
body.stories .grid{display:block;margin:0;height:calc(100vh - 62px);overflow-y:auto;scroll-snap-type:y mandatory}
body.stories .fc{scroll-snap-align:start;height:calc(100vh - 62px);aspect-ratio:auto;border-radius:0;max-width:560px;margin:0 auto;box-shadow:none}
body.stories .fc h3{font-size:30px}body.stories .fc p{font-size:15px}
.empty{border:1px dashed var(--line);border-radius:22px;padding:40px;text-align:center;color:var(--muted);margin-top:18px}
"""

PAGE = head("Feed · facelab", CSS) + "<body>" + nav("feed") + r"""
<div class="wrap">
<div class="top-row"><div><div class="eyebrow">Feed</div><h2>Personas que ya<br><span class="light">se analizaron.</span></h2><p class="lede" style="margin-top:8px">Cada tarjeta resume un informe real: puntuación global, estación de color, forma de cara y lo que juega a su favor. Toca para ver el informe completo.</p></div>
<div class="tabs"><button class="on" onclick="mode('grid',this)">Rejilla</button><button onclick="mode('stories',this)">Historias</button></div></div>
<div class="grid" id="grid"></div>
<footer style="margin-top:80px;border-top:1px solid var(--line);padding-top:18px;font-size:12px;color:var(--muted);max-width:80ch">Los resultados son lecturas estadísticas de una foto. No hay notas de belleza: la puntuación global combina marcos medidos y se explica en cada informe.</footer>
</div>
<script>
function mode(m,el){document.body.classList.toggle('stories',m==='stories');[...el.parentNode.children].forEach(b=>b.classList.toggle('on',b===el))}
const SEX={male:'hombre',female:'mujer'};
fetch('/api/feed').then(r=>r.json()).then(l=>{const g=document.getElementById('grid');if(!l.length){g.innerHTML='<div class="empty">Aún no hay análisis. <a href="/#analizar">Sé la primera persona.</a></div>';return}
g.innerHTML=l.map(x=>`<a class="fc" href="/report/${x.stem}">${x.face?'<img src="/out/'+x.face+'" alt="">':''}
<div class="top"><span class="who"><span>${(x.name||'?')[0].toUpperCase()}</span>${x.name||'Anónimo'}</span>${x.global!=null?'<span class="sc">'+x.global+'<small>/100</small></span>':''}</div>
<div class="ov"><h3>${x.headline||'Análisis facial'}</h3><p>${x.strength||''}</p><div class="chips">${x.season?'<span class="chip"><i style="background:'+(x.season_hex||'#fff')+'"></i>'+x.season+'</span>':''}${x.face_shape?'<span class="chip">Cara '+x.face_shape.toLowerCase()+'</span>':''}${x.visual_age?'<span class="chip">Edad visual '+x.visual_age+'</span>':''}${x.profile?'<span class="chip">'+[SEX[x.profile.sex],x.profile.age?x.profile.age+' años':''].filter(Boolean).join(' · ')+'</span>':''}</div>
<div class="bars">${[['Simetría',x.symmetry],['Proporción',x.proportionality],['Averageness',x.averageness]].filter(b=>b[1]!=null).map(([k,v])=>`<div class="bar"><small>${k}</small><b>${v}</b><i style="--w:${v}%"></i></div>`).join('')}</div></div>
${x.reviewed?'<span class="rev">Revisado</span>':''}</a>`).join('')});
</script></body></html>"""
