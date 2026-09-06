from .ui import head, nav
"""Páginas de administración: cola de revisión (editar y aprobar narrativa y protocolo), personas y comparación."""
ADMIN = head("Revisión · facelab", r"""
.wrap{max-width:1100px;margin:0 auto;padding:28px}h1{font-size:28px;letter-spacing:-.02em;margin:0 0 6px}h2{font-size:18px;margin:26px 0 8px}h3{font-size:14px;margin:14px 0 6px;color:var(--accent);text-transform:uppercase;letter-spacing:.1em}
a{color:var(--accent)}.muted{color:var(--muted);font-size:13px}
table{border-collapse:collapse;width:100%;font-size:14px}th{text-align:left;font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);padding:8px;border-bottom:1px solid var(--ink)}td{padding:8px;border-bottom:1px solid var(--line);vertical-align:middle}
.badge{font-size:11px;padding:2px 8px;border-radius:6px;background:var(--amber2);color:var(--amber);font-weight:700}.badge.ok{background:var(--accent2);color:var(--accent)}
.face{width:44px;height:44px;border-radius:8px;object-fit:cover;background:var(--panel)}
textarea,input[type=text]{width:100%;font:14px Manrope,system-ui;padding:8px 10px;border:1px solid var(--line);border-radius:8px;background:#fff;box-sizing:border-box}textarea{min-height:72px;resize:vertical}
.card{background:#fff;border:1px solid var(--line);border-radius:12px;padding:14px 16px;margin-bottom:12px}
.row{display:grid;grid-template-columns:200px 1fr;gap:10px;align-items:start;margin-bottom:8px}.row label{font-size:12px;color:var(--muted);padding-top:8px}
button{font:600 13px Manrope,system-ui;padding:8px 14px;border:1px solid var(--accent);background:var(--accent);color:#fff;border-radius:10px;cursor:pointer}button.ghost{background:#fff;color:var(--accent)}
.bar{position:sticky;top:0;background:rgba(251,251,250,.92);backdrop-filter:blur(8px);border-bottom:1px solid var(--line);padding:10px 0;margin-bottom:18px;display:flex;gap:10px;align-items:center;flex-wrap:wrap}
.ok{color:var(--accent);font-size:13px}
""") + "<body>" + nav("admin") + r"""<div class="wrap" id="app">Cargando…</div>
<script>
const parts=location.pathname.split('/').filter(Boolean);const stem=parts[1];
const esc=s=>String(s??'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/"/g,'&quot;');
async function list(){const l=await (await fetch('/reports')).json();
document.getElementById('app').innerHTML=`<h1>Cola de revisión</h1><p class="muted">Cada informe se edita y aprueba antes de marcarlo como revisado. <a href="/people">Personas y seguimiento</a> · <a href="/">Subir foto</a></p>
<table><tr><th></th><th>Informe</th><th>Persona</th><th>Perfil</th><th>Estado</th><th></th></tr>${l.map(r=>`<tr><td>${r.face?`<img class="face" src="/out/${r.face}">`:''}</td><td><a href="/report/${r.stem}">${r.stem}</a><div class="muted">${r.date||''}</div></td><td>${esc(r.person||'—')}</td><td class="muted">${(r.profile||{}).sex||'?'} · ${(r.profile||{}).ancestry||'?'}</td><td>${r.review&&r.review.approved?'<span class="badge ok">revisado</span>':r.has_narrative?'<span class="badge">pendiente</span>':'<span class="muted">generando</span>'}</td><td><a href="/admin/${r.stem}"><button class="ghost">Revisar</button></a></td></tr>`).join('')}</table>`}
let R=null;
function ta(path,val,rows=3){return `<textarea data-path="${path}" rows="${rows}">${esc(val)}</textarea>`}
function get(o,p){return p.split('.').reduce((a,k)=>a==null?a:a[isNaN(k)?k:+k],o)}
function setp(o,p,v){const ks=p.split('.');let a=o;for(let i=0;i<ks.length-1;i++){const k=isNaN(ks[i])?ks[i]:+ks[i];a=a[k]}a[isNaN(ks.at(-1))?ks.at(-1):+ks.at(-1)]=v}
async function edit(){R=await (await fetch('/api/report/'+stem)).json();const n=R.narrative||{},P=R.protocol||{},rv=R.review||{};
let h=`<div class="bar"><a href="/admin">← Cola</a><b>${stem}</b><span class="muted">${esc(R.person||'')}</span><span style="margin-left:auto"></span><input type="text" id="reviewer" placeholder="Tu nombre" value="${esc(rv.by||'')}" style="width:160px"><button class="ghost" onclick="save(false)">Guardar</button><button onclick="save(true)">Guardar y aprobar</button><span class="ok" id="msg">${rv.approved?'Revisado por '+esc(rv.by)+' · '+esc(rv.at):''}</span></div>
<div style="display:grid;grid-template-columns:220px 1fr;gap:20px"><div><img src="/out/${(R.assets||{}).face||''}" style="width:100%;border-radius:12px"><p class="muted">${(R.norms||{}).group||''} · edad visual ${(R.age||{}).visual_age||'?'}</p><a href="/report/${stem}" target="_blank">Ver informe →</a></div><div>`;
h+='<h2>Notas del revisor</h2>'+ta('review.notes',rv.notes||'',2);
h+='<h2>Narrativa</h2>';for(const [sec,v] of Object.entries(n)){h+=`<div class="card"><h3>${sec.replace(/_/g,' ')}</h3><div class="row"><label>Resumen</label>${ta('narrative.'+sec+'.summary',v.summary,3)}</div>${(v.findings||[]).map((f,i)=>`<div class="row"><label>${esc(f.measure)}</label>${ta('narrative.'+sec+'.findings.'+i+'.statement',f.statement,2)}</div>`).join('')}<div class="row"><label>Puntos fuertes (uno por línea)</label>${ta('narrative.'+sec+'.strengths',(v.strengths||[]).join('\n'),2)}</div><div class="row"><label>A vigilar (uno por línea)</label>${ta('narrative.'+sec+'.watch',(v.watch||[]).join('\n'),2)}</div></div>`}
h+='<h2>Protocolo</h2>';(P.phases||[]).forEach((ph,i)=>{h+=`<div class="card"><h3>${esc(ph.name)} · ${esc(ph.weeks)}</h3><div class="row"><label>Objetivo</label>${ta('protocol.phases.'+i+'.goal',ph.goal,2)}</div>${(ph.actions||[]).map((a,j)=>`<div class="row"><label>${esc(a.name)}</label>${ta('protocol.phases.'+i+'.actions.'+j+'.why',a.why,2)}</div>`).join('')}</div>`});
h+=`<div class="card"><h3>No hace falta tocar (uno por línea)</h3>${ta('protocol.not_recommended',(P.not_recommended||[]).join('\n'),3)}<h3>Carta</h3>${ta('protocol.letter',P.letter||'',5)}</div>`;
h+='</div></div>';document.getElementById('app').innerHTML=h}
async function save(approve){const patch={narrative:R.narrative||{},protocol:R.protocol||{},review:{...(R.review||{})}};
document.querySelectorAll('textarea[data-path]').forEach(t=>{const p=t.dataset.path;const listy=/\.(strengths|watch)$|not_recommended$/.test(p);const v=listy?t.value.split('\n').map(s=>s.trim()).filter(Boolean):t.value;if(p.startsWith('review.'))patch.review[p.slice(7)]=v;else setp(patch,p,v)});
patch.review.by=document.getElementById('reviewer').value||patch.review.by||'';if(approve){patch.review.approved=true;patch.review.at=new Date().toISOString().slice(0,16).replace('T',' ')}
const r=await fetch('/api/review/'+stem,{method:'PUT',headers:{'Content-Type':'application/json'},body:JSON.stringify(patch)});const j=await r.json();document.getElementById('msg').textContent=j.error?('Error: '+j.error):(approve?'Aprobado y guardado':'Guardado');if(!j.error)R=await (await fetch('/api/report/'+stem)).json()}
stem?edit():list();
</script></body></html>"""

PEOPLE = head("Personas · facelab", r"""
h1{font-size:28px;letter-spacing:-.02em;margin:0 0 6px}h2{font-size:20px;margin:28px 0 8px}a{color:var(--accent)}.muted{color:var(--muted);font-size:13px}
.person{background:#fff;border:1px solid var(--line);border-radius:12px;padding:14px 16px;margin-bottom:12px}
.tl{display:flex;gap:12px;overflow-x:auto;padding:6px 0}.rep{width:180px;flex:0 0 180px;border:1px solid var(--line);border-radius:10px;padding:10px;background:var(--paper)}.rep img{width:100%;aspect-ratio:1;object-fit:cover;border-radius:8px}.rep .d{font-size:12px;color:var(--muted);margin:6px 0 2px}
.sc{font-size:12px;display:grid;grid-template-columns:1fr auto;gap:2px 8px}
button{font:600 13px Manrope,system-ui;padding:6px 12px;border:1px solid var(--accent);background:#fff;color:var(--accent);border-radius:8px;cursor:pointer}
table{border-collapse:collapse;width:100%;font-size:14px}th{text-align:left;font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);padding:8px;border-bottom:1px solid var(--ink)}td{padding:8px;border-bottom:1px solid var(--line);font-variant-numeric:tabular-nums}
.up{color:var(--accent);font-weight:700}.down{color:var(--amber);font-weight:700}.faces{display:grid;grid-template-columns:1fr 1fr;gap:14px;max-width:560px}.faces img{width:100%;border-radius:12px}
""") + "<body>" + nav("people") + r"""<div class="wrap" id="app">Cargando…</div>
<script>
const q=new URLSearchParams(location.search);const esc=s=>String(s??'').replace(/</g,'&lt;');
async function people(){const l=await (await fetch('/reports')).json();const g={};for(const r of l){const k=r.person||'(sin nombre)';(g[k]=g[k]||[]).push(r)}
let h=`<h1>Personas y seguimiento</h1><p class="muted">Cada persona con sus informes en el tiempo. Elige dos para comparar. <a href="/admin">Cola de revisión</a> · <a href="/">Subir foto</a></p>`;
for(const [k,rs] of Object.entries(g)){rs.sort((a,b)=>(a.date||'').localeCompare(b.date||''));h+=`<div class="person"><h2 style="margin:0 0 6px">${esc(k)} <span class="muted">· ${rs.length} informe${rs.length>1?'s':''}</span></h2><div class="tl">${rs.map(r=>`<div class="rep"><img src="${r.face?'/out/'+r.face:''}"><div class="d">${r.date||''}</div><div class="sc">${Object.entries(r.scores||{}).map(([a,b])=>`<span>${a}</span><b>${b}</b>`).join('')}</div><div style="margin-top:8px;display:flex;gap:6px"><a href="/report/${r.stem}"><button>Ver</button></a><label style="font-size:12px;display:flex;align-items:center;gap:4px"><input type="checkbox" name="cmp" value="${r.stem}">comparar</label></div></div>`).join('')}</div><button onclick="go()">Comparar seleccionados</button></div>`}
document.getElementById('app').innerHTML=h}
function go(){const s=[...document.querySelectorAll('input[name=cmp]:checked')].map(i=>i.value);if(s.length!==2){alert('Selecciona exactamente dos informes');return}location.href='/compare?a='+s[0]+'&b='+s[1]}
async function compare(){const [A,B]=await Promise.all([q.get('a'),q.get('b')].map(s=>fetch('/api/report/'+s).then(r=>r.json())));
const d=x=>x.date||'';const rows=[];const pa=(A.norms||{}).per_measure||{},pb=(B.norms||{}).per_measure||{};
for(const k of Object.keys(pa)){if(!pb[k])continue;rows.push([k,pa[k].percentile,pb[k].percentile])}
const S=['symmetry','averageness','proportionality'];let h=`<h1>Comparación</h1><p class="muted"><a href="/people">← Personas</a> · ${esc(A.person||'')} · ${d(A)} → ${d(B)}</p><div class="faces"><div><img src="/out/${A.assets.face}"><div class="muted">${d(A)}</div></div><div><img src="/out/${B.assets.face}"><div class="muted">${d(B)}</div></div></div>`;
h+='<h2>Scores</h2><table><tr><th>Score</th><th>Antes</th><th>Después</th><th>Δ</th></tr>'+S.map(k=>{const a=(A.scores||{})[k]||{},b=(B.scores||{})[k]||{};const va=a.score,vb=b.score;const dl=(vb-va);return `<tr><td>${k}</td><td>${va}</td><td>${vb}</td><td class="${dl>0?'up':dl<0?'down':''}">${dl>0?'+':''}${dl.toFixed(1)}</td></tr>`}).join('')+`<tr><td>edad visual</td><td>${(A.age||{}).visual_age??'–'}</td><td>${(B.age||{}).visual_age??'–'}</td><td></td></tr></table>`;
const sk=k=>((A.skin||{})[k]!=null&&(B.skin||{})[k]!=null)?`<tr><td>${k}</td><td>${A.skin[k]}</td><td>${B.skin[k]}</td><td class="${B.skin[k]<A.skin[k]?'up':'down'}">${(B.skin[k]-A.skin[k]).toFixed(2)}</td></tr>`:'';
h+='<h2>Piel (menos es mejor)</h2><table><tr><th>Métrica</th><th>Antes</th><th>Después</th><th>Δ</th></tr>'+['redness_pct','spots_pct','texture_index','shine_pct','tone_unevenness'].map(sk).join('')+'</table>';
rows.sort((x,y)=>Math.abs(y[2]-y[1])-Math.abs(x[2]-x[1]));h+='<h2>Percentiles por medida (mayor cambio primero)</h2><table><tr><th>Medida</th><th>Antes</th><th>Después</th><th>Δ</th></tr>'+rows.slice(0,25).map(([k,a,b])=>`<tr><td>${((A.catalog[k.split('.')[0]]||{}).name||k)}${k.includes('.')?' · '+k.split('.')[1]:''}</td><td>p${Math.round(a)}</td><td>p${Math.round(b)}</td><td>${(b-a)>0?'+':''}${(b-a).toFixed(0)}</td></tr>`).join('')+'</table><p class="muted">Los percentiles comparan con el mismo grupo de referencia; cambios menores de ±10 puntos entran en el ruido de medida entre fotos (luz, pose y expresión).</p>';
document.getElementById('app').innerHTML=h}
location.pathname.startsWith('/compare')?compare():people();
</script></body></html>"""
