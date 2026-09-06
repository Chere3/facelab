"use client";
import { useEffect, useState } from "react";
import Link from "next/link";
import { getFeed, out } from "@/lib/api";
import type { FeedItem } from "@/lib/types";
import { Nav } from "@/components/site/Nav";
import { Chip } from "@/components/site/Chip";
import { BeforeAfter } from "@/components/charts/BeforeAfter";
import { Onboarding } from "@/components/landing/Onboarding";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

const FEATURES = [
  ["📐", "Medidas de tu cara", "478 puntos, 32 proporciones: tercios, quintos, ojos, nariz, boca, mandíbula, simetría.", "Farkas 1994 · Naini 2011"],
  ["📊", "Comparadas con tu grupo", "Cada medida con su percentil frente a personas de tu mismo sexo y ascendencia.", "MEBeauty · Rhodes 2006"],
  ["✨", "Piel y edad visual", "Mapas de rojez, manchas, textura y brillo, y una edad visual con su margen de error.", "SegFormer · InsightFace"],
  ["🎨", "Colores y estilo", "Tu estación de color, paleta, forma de cara, la misma foto con 16 camisas, armario, looks y cortes.", "Jackson 1980 · Russell 2009"],
  ["🗓️", "Tu rutina por fases", "Entre 4 y 16 acciones no quirúrgicas con evidencia, coste y frecuencia, hasta 12 meses.", "Biblioteca de 53 métodos"],
  ["👤", "Perfil real", "Con una foto lateral: nariz, labios y mentón medidos sobre la silueta real.", "Ricketts · Legan & Burstone"],
];
const FAQ = [
  ["¿Me va a decir si soy guapo o guapa?", "No. facelab mide proporciones, colores y piel, y las compara con personas parecidas a ti. Hay una lectura global estadística, pero se muestra con todos sus componentes y con un aviso claro de que es una lectura de una foto, no una nota."],
  ["¿Qué foto necesito?", "Una de frente, con luz de día, sin gafas ni gorro, boca cerrada y sin filtros. Si añades una de perfil a 90°, medimos también los ángulos reales de nariz, labios y mentón."],
  ["¿Adónde van mis fotos?", "Se procesan y se guardan en el ordenador donde corre facelab. Solo el texto de la narrativa y de la rutina pasa por la IA. Puedes elegir no aparecer en el feed."],
  ["¿Cuánto tarda?", "Las medidas salen en segundos. El informe se abre al instante y se completa solo en unos cinco minutos: narrativa, rutina, proyección y looks."],
  ["¿Es un diagnóstico médico?", "No. Es un análisis geométrico y de color sobre una foto. Cualquier procedimiento o principio activo de la rutina se consulta con un profesional."],
];

export default function Landing() {
  const [open, setOpen] = useState(false);
  const [feed, setFeed] = useState<FeedItem[]>([]);
  useEffect(() => { getFeed().then(setFeed).catch(() => {}); }, []);
  useEffect(() => {
    const check = () => { if (location.hash === "#analizar") setOpen(true); };
    check(); window.addEventListener("hashchange", check); return () => window.removeEventListener("hashchange", check);
  }, []);
  const hero = feed.find((x) => x.face);
  const tr = feed.filter((x) => x.after && x.face).slice(0, 3);
  const n = feed.length;

  return (
    <div className="bg-blobs">
      <Nav cta={false}><nav className="hidden gap-4 text-[13px] text-muted-foreground md:ml-6 md:flex">{[["#tu-cara", "Tu cara"], ["#transformaciones", "Transformaciones"], ["#guia", "Qué mide"], ["#planes", "Planes"]].map(([h, l]) => <a key={h} href={h} className="hover:text-ink">{l}</a>)}</nav><Button className="ml-auto rounded-full md:ml-0" onClick={() => setOpen(true)}>Analizar mi cara</Button></Nav>
      <main className="mx-auto max-w-[1240px] px-5 md:px-7">
        {/* hero */}
        <div className="grid min-h-[calc(100vh-60px)] items-center gap-8 py-10 md:grid-cols-[minmax(0,5fr)_minmax(0,6fr)]">
          <div className="animate-in fade-in slide-in-from-bottom-3 duration-700">
            <div className="mb-5 inline-flex items-center gap-2.5"><span className="flex">{feed.slice(0, 4).map((x, i) => x.face ? <img key={x.stem} src={out(x.face)} alt="" className={cn("size-7 rounded-full border-2 border-paper object-cover", i && "-ml-2")} /> : null)}</span><Chip>{n ? `${n} persona${n > 1 ? "s" : ""} ya se lo ${n > 1 ? "hicieron" : "hizo"}` : "Sé la primera persona en analizarte"}</Chip></div>
            <h1 className="text-[clamp(44px,6vw,84px)] leading-[0.95] font-medium">Descubre lo que tu cara <em className="italic text-coral">ya dice de ti.</em></h1>
            <p className="mt-5 max-w-[46ch] text-[17px] text-muted-foreground">Medimos tu cara, tus colores y tu piel, lo comparamos con personas parecidas a ti y te decimos qué te favorece. En palabras que cualquiera entiende, con la ciencia a un clic.</p>
            <div className="mt-7 flex flex-wrap gap-2.5"><Button size="lg" className="h-12 rounded-full px-6 text-[15px]" onClick={() => setOpen(true)}>Analizar mi cara</Button><Link href="/feed"><Button size="lg" variant="outline" className="h-12 rounded-full px-6 text-[15px]">Ver transformaciones</Button></Link></div>
            <p className="mt-4 text-[12px] text-muted-foreground">≈ 5 minutos · se procesa en tu ordenador · sin notas de belleza</p>
          </div>
          <div className="relative mx-auto aspect-square w-full max-w-[600px] animate-in fade-in zoom-in-95 duration-1000">
            <div className="absolute inset-0 overflow-hidden rounded-[48px]" style={{ background: "radial-gradient(60% 60% at 50% 45%, #ffe1e6, #fbf7f2 80%)" }}>
              {hero && <img src={out(hero.face)} alt="" className="size-full object-cover" style={{ maskImage: "radial-gradient(62% 60% at 50% 44%, #000 34%, transparent 72%)", WebkitMaskImage: "radial-gradient(62% 60% at 50% 44%, #000 34%, transparent 72%)" }} />}
            </div>
            {hero && <>
              <Float style={{ left: "-2%", top: "16%" }} dot={hero.season_hex || "#e9506a"}>{hero.season || "Otoño profundo"}</Float>
              <Float style={{ right: "0", top: "28%", animationDelay: "1s" }} dot="var(--sage)">{hero.face_shape ? `Cara ${hero.face_shape.toLowerCase()}` : "Cara ovalada"}</Float>
              <Float style={{ left: "6%", bottom: "12%", animationDelay: "2s" }} dot="var(--lavender)">{hero.symmetry != null ? `Simetría ${Math.round(hero.symmetry)}` : "Simetría"}</Float>
            </>}
          </div>
        </div>

        <div className="grid grid-cols-2 gap-4 md:grid-cols-4">{[["32", "medidas faciales con percentil"], ["1638", "caras de referencia de seis ascendencias"], ["12", "estaciones de color y 16 camisas"], ["13", "looks y cortes sobre tu foto"]].map(([b, s]) => <div key={b} className="card-soft p-5"><b className="font-display text-[40px] leading-none font-medium">{b}</b><small className="mt-1.5 block text-[13px] text-muted-foreground">{s}</small></div>)}</div>

        {/* IA */}
        <div id="tu-cara" className="mt-28 grid overflow-hidden rounded-[40px] shadow-lift md:min-h-[560px] md:grid-cols-2">
          <div className="relative min-h-[360px] bg-secondary">{hero && <img src={out(hero.look || hero.face)} alt="" className="absolute inset-0 size-full object-cover" />}</div>
          <div className="flex flex-col items-center bg-gradient-to-b from-peach-2 via-cream to-paper px-8 py-16 text-center md:px-14 md:py-24"><h2 className="text-[clamp(30px,3.6vw,46px)] font-medium">Análisis facial <em className="italic text-coral">con IA.</em></h2><p className="mt-3 max-w-[42ch] text-[15px] text-ink-2">La IA no promete perfección: observa, mide y explica. Cada análisis lee tu cara tal como es hoy y señala, con datos, qué merece atención y qué juega a tu favor.</p></div>
        </div>

        <div className="py-32 text-center md:py-40"><h2 className="mx-auto max-w-[24ch] text-[clamp(30px,4.2vw,58px)] leading-[1.08] font-normal text-muted-foreground">facelab te ayuda a <b className="font-medium text-ink">entender tu cara</b> como nunca: medidas reales, <b className="font-medium text-ink">explicadas para cualquiera</b> y respaldadas por <b className="font-medium text-ink">ciencia publicada</b>, no por opiniones.</h2></div>

        {/* transformaciones */}
        <section id="transformaciones" className="scroll-mt-24">
          <Head eyebrow="Transformaciones" title={<>Antes y después, <em className="italic text-coral">sin cirugía.</em></>} lede="Proyecciones generadas sobre la foto real de cada persona a partir de su rutina: piel, cejas, pelo, descanso, ropa. Arrastra para comparar." />
          <div className="mt-8 grid gap-5 md:grid-cols-3">{tr.length ? tr.map((x) => <div key={x.stem}><BeforeAfter before={out(x.face)} after={out(x.after)} ratio="4/5" labels={["Antes", "Proyección"]} className="shadow-soft" /><div className="mt-2.5 flex items-center justify-between text-[13px]"><b>{x.name || "Anónimo"}</b><Link href={`/report/${x.stem}`} className="font-semibold text-coral">Ver informe →</Link></div></div>) : <p className="text-[13px] text-muted-foreground">Las transformaciones aparecen cuando un informe termina su proyección.</p>}</div>
        </section>

        {/* guía */}
        <section id="guia" className="mt-28 scroll-mt-24">
          <Head eyebrow="Qué mide" title={<>Todo lo que mide, <em className="italic text-coral">y para qué sirve.</em></>} lede="Seis módulos que trabajan sobre la misma foto. Cada uno cita su fuente y devuelve percentiles dentro de tu grupo." />
          <div className="mt-8 grid gap-4 sm:grid-cols-2 md:grid-cols-3">{FEATURES.map(([ic, t, d, src]) => <div key={t} className="card-soft flex min-h-[200px] flex-col p-6"><span className="mb-4 flex size-10 items-center justify-center rounded-2xl bg-coral-2 text-[18px]">{ic}</span><h3 className="text-[18px] font-semibold">{t}</h3><p className="mt-1 text-[14px] text-muted-foreground">{d}</p><div className="mt-auto pt-4 text-[11px] font-semibold text-coral">{src}</div></div>)}</div>
        </section>

        {/* filosofía */}
        <section className="mt-28 grid gap-10 md:grid-cols-[minmax(0,1fr)_minmax(0,1.2fr)]">
          <div><div className="eyebrow mb-2">Filosofía</div><h2 className="text-[clamp(28px,3.4vw,42px)] font-medium">Datos, <em className="italic text-coral">no juicios.</em></h2><p className="mt-3 max-w-[40ch] text-[16px] text-muted-foreground">Medimos y explicamos. Nunca decimos si alguien es guapo: decimos qué mide, cómo se compara y qué se puede hacer.</p></div>
          <ol className="divide-y divide-line">{[["Sin notas de belleza", "Cada frase se apoya en un valor, un percentil y una norma citada. Los scores globales se explican con todos sus componentes y sus pesos."], ["Ciencia con fuentes", "Farkas, Naini, Ricketts, Rhodes, Russell, Perrett. Si un dato es orientativo, lo decimos y explicamos por qué."], ["Privado por diseño", "Las fotos y los informes se procesan y se guardan en tu ordenador. Solo el texto redactado por la IA sale a internet."], ["Revisión humana", "Cada informe puede pasar por una cola de revisión donde una persona corrige, aprueba y firma antes de entregarlo."]].map(([t, d], i) => <li key={t} className="grid grid-cols-[48px_1fr] gap-3 py-5"><span className="text-[13px] font-bold tracking-widest text-coral">0{i + 1}</span><div><b className="block text-[17px]">{t}</b><p className="mt-1 text-[14px] text-muted-foreground">{d}</p></div></li>)}</ol>
        </section>

        {/* planes */}
        <section id="planes" className="mt-28 scroll-mt-24">
          <Head eyebrow="Planes" title={<>Para ti, <em className="italic text-coral">y para tu equipo.</em></>} lede="El análisis personal es gratuito y local. Los planes de estudio y clínica añaden revisión humana, seguimiento y marca propia." />
          <div className="mt-8 grid gap-4 md:grid-cols-3">
            <Plan name="Personal" price="Gratis" sub="en tu ordenador" desc="Informe completo con medidas, colorimetría, rutina y looks." items={["32 medidas con percentil", "Colorimetría y 16 camisas", "Rutina por fases", "13 looks renderizados", "PDF y tarjetas para compartir"]} cta={<Button className="mt-auto w-full rounded-full" onClick={() => setOpen(true)}>Analizar mi cara</Button>} />
            <Plan dark name="Estudio" price="Próximamente" desc="Para estilistas, asesores de imagen y centros de estética." items={["Cola de revisión y firma", "Seguimiento por persona", "Comparación entre informes", "Feed privado con tu marca", "Exportación en lote"]} cta={<a href="#contacto"><Button variant="outline" className="mt-auto w-full rounded-full border-white bg-white text-ink hover:bg-cream">Avísame</Button></a>} />
            <Plan name="Clínica" price="A medida" desc="Integración con tu flujo clínico y normas propias." items={["Normas con tu propia población", "Perfil lateral y cefalometría de tejido blando", "Biblioteca de métodos ampliable", "Despliegue en tus equipos"]} cta={<a href="#contacto"><Button variant="outline" className="mt-auto w-full rounded-full">Hablar con nosotros</Button></a>} />
          </div>
        </section>

        {/* faq */}
        <section className="mt-28"><div className="eyebrow mb-2">Preguntas</div><h2 className="text-[clamp(28px,3.4vw,42px)] font-medium">Lo que todo el mundo <em className="italic text-coral">pregunta primero.</em></h2>
          <div className="mt-5 max-w-[760px] divide-y divide-line">{FAQ.map(([q, a], i) => <details key={q} open={!i} className="group py-4"><summary className="flex cursor-pointer list-none items-center justify-between text-[16px] font-semibold">{q}<span className="text-[20px] font-light text-muted-foreground group-open:hidden">+</span><span className="hidden text-[20px] font-light text-muted-foreground group-open:inline">–</span></summary><p className="mt-2 max-w-[62ch] text-[14px] text-muted-foreground">{a}</p></details>)}</div></section>

        <div className="mt-32 rounded-[40px] px-8 py-20 text-center" style={{ background: "radial-gradient(80% 120% at 50% 0%, #ffe1e6, #fbf7f2 70%)" }}><div className="eyebrow mb-2">Empieza ahora</div><h2 className="text-[clamp(34px,5vw,66px)] font-medium">Tu cara, medida <em className="italic text-coral">y explicada.</em></h2><p className="mx-auto mt-3 mb-7 max-w-[40ch] text-muted-foreground">Cinco minutos. Sin registro. Sin notas de belleza.</p><Button size="lg" className="h-12 rounded-full px-7 text-[15px]" onClick={() => setOpen(true)}>Analizar mi cara</Button></div>

        <footer id="contacto" className="mt-24 grid gap-8 border-t border-line py-10 text-[13px] text-muted-foreground md:grid-cols-[2fr_1fr_1fr_1fr]">
          <div><span className="font-display text-[16px] font-semibold text-ink">facelab</span><p className="mt-2 max-w-[44ch]">Morfometría facial, colorimetría y estilo sobre una foto, explicados para cualquiera. No presta servicios clínicos ni médicos.</p></div>
          <div><b className="mb-2 block text-ink">Producto</b>{[["#tu-cara", "Tu cara"], ["#transformaciones", "Transformaciones"], ["#guia", "Qué mide"], ["#planes", "Planes"]].map(([h, l]) => <a key={h} href={h} className="block py-0.5 hover:text-ink">{l}</a>)}</div>
          <div><b className="mb-2 block text-ink">Herramientas</b>{[["/feed", "Feed"], ["/people", "Personas"], ["/admin", "Revisión"]].map(([h, l]) => <Link key={h} href={h} className="block py-0.5 hover:text-ink">{l}</Link>)}</div>
          <div><b className="mb-2 block text-ink">Contacto</b><a href="mailto:hola@facelab.local" className="block py-0.5 hover:text-ink">hola@facelab.local</a><a href="https://github.com/Chere3/facelab" target="_blank" rel="noopener" className="block py-0.5 hover:text-ink">GitHub</a></div>
        </footer>
      </main>
      <Onboarding open={open} onOpenChange={(o) => { setOpen(o); if (!o && location.hash === "#analizar") history.replaceState(null, "", " "); }} />
    </div>
  );
}

function Float({ children, dot, style }: { children: React.ReactNode; dot: string; style: React.CSSProperties }) {
  return <span className="absolute inline-flex items-center gap-2 rounded-full border border-line bg-paper px-3 py-1.5 text-[12px] font-semibold shadow-soft motion-safe:animate-[bob_4s_ease-in-out_infinite]" style={style}><i className="size-2 rounded-full" style={{ background: dot }} />{children}<style>{`@keyframes bob{0%,100%{transform:translateY(0)}50%{transform:translateY(-6px)}}`}</style></span>;
}
function Head({ eyebrow, title, lede }: { eyebrow: string; title: React.ReactNode; lede: string }) {
  return <div className="grid gap-4 md:grid-cols-2 md:items-end"><div><div className="eyebrow mb-2">{eyebrow}</div><h2 className="text-[clamp(28px,3.4vw,42px)] leading-[1.02] font-medium">{title}</h2></div><p className="text-[16px] text-muted-foreground">{lede}</p></div>;
}
function Plan({ name, price, sub, desc, items, cta, dark }: { name: string; price: string; sub?: string; desc: string; items: string[]; cta: React.ReactNode; dark?: boolean }) {
  return <div className={cn("flex flex-col rounded-[28px] border p-7", dark ? "border-ink bg-ink text-white" : "border-line bg-paper")}><div className={cn("text-[12px] font-bold tracking-[0.14em] uppercase", dark ? "text-peach" : "text-coral")}>{name}</div><div className="mt-2 font-display text-[40px] leading-none font-medium">{price}{sub && <small className="ml-1 text-[13px] font-normal opacity-70">· {sub}</small>}</div><p className="mt-2 mb-4 text-[14px] opacity-80">{desc}</p><ul className="mb-6 text-[14px]">{items.map((x) => <li key={x} className="flex gap-2.5 border-t border-current/15 py-1.5"><span className={cn("font-bold", dark ? "text-peach" : "text-coral")}>✓</span>{x}</li>)}</ul>{cta}</div>;
}
