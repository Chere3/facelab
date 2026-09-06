import type { Report } from "@/lib/types";
import { out } from "@/lib/api";
import { COMP, highlights } from "@/lib/plain";

/* Tarjetas 9:16 (1080×1920). Se usan a escala en el informe y a tamaño real en /story/<stem> para capturar PNG. */
const BG = ["radial-gradient(120% 70% at 50% 0%, #ffe1e6 0%, #fbf7f2 60%)", "radial-gradient(120% 70% at 50% 100%, #ece7ff 0%, #fbf7f2 60%)", "radial-gradient(100% 60% at 0% 0%, #fff0e6 0%, #fbf7f2 60%)"];

function Frame({ bg = 0, eyebrow, title, children, foot }: { bg?: number; eyebrow: string; title: React.ReactNode; children?: React.ReactNode; foot: [string, string] }) {
  return (
    <div className="story relative overflow-hidden text-ink" style={{ width: 1080, height: 1920, background: BG[bg % BG.length], fontFamily: "var(--font-figtree)" }}>
      <div className="absolute inset-0 flex flex-col" style={{ padding: "96px 84px" }}>
        <div className="flex items-center gap-3.5 font-display text-[34px] font-semibold tracking-tight"><span className="inline-block size-10 rounded-[30%]" style={{ background: "conic-gradient(from 200deg, var(--coral), var(--peach), var(--butter), var(--lavender), var(--coral))" }} />facelab</div>
        <div className="mt-[72px] mb-4 text-[22px] font-bold tracking-[0.18em] text-coral uppercase">{eyebrow}</div>
        <h1 className="font-display text-[108px] leading-[0.96] font-medium tracking-tight" style={{ marginBottom: 28 }}>{title}</h1>
        {children}
        <div className="mt-auto flex items-end justify-between text-[24px] text-muted-foreground"><span>{foot[0]}</span><b className="text-ink">{foot[1]}</b></div>
      </div>
    </div>
  );
}
const P = ({ children }: { children: React.ReactNode }) => <p className="text-[34px] leading-[1.35] text-ink-2">{children}</p>;
const ChipL = ({ children, hex }: { children: React.ReactNode; hex?: string }) => <span className="inline-flex items-center gap-3.5 rounded-full border-2 border-line bg-paper px-7 py-4 text-[28px] font-semibold">{hex && <i className="inline-block size-[22px] rounded-full" style={{ background: hex }} />}{children}</span>;
const Img = ({ src, alt = "" }: { src: string; alt?: string }) => <img src={src} alt={alt} className="size-full object-cover" />;

export function storyCards(R: Report): React.ReactNode[] {
  const s = R.scores || {}, st = R.style || {}, G = s.global?.composite, face = out(R.assets?.face), name = R.person || "Tu cara";
  const { strengths } = highlights(R);
  const cards: React.ReactNode[] = [];
  cards.push(
    <Frame key="hero" eyebrow="Análisis facial" title={<>{name},<br /><em className="italic text-coral">medida y explicada.</em></>} foot={["Medido con IA · orientativo", R.date || ""]}>
      <P>{Object.keys(R.norms?.per_measure || {}).length} medidas comparadas con {R.norms?.n ?? 0} caras. Sin notas de belleza: datos y explicaciones.</P>
      <div className="mt-10 aspect-square w-full overflow-hidden rounded-[56px] bg-secondary shadow-lift">{face && <Img src={face} />}</div>
      <div className="mt-8 flex flex-wrap gap-4">{s.symmetry && <ChipL>Simetría p{Math.round(s.symmetry.percentile)}</ChipL>}{st.season && <ChipL hex={st.palette?.best?.[0]?.hex}>{st.season.name}</ChipL>}{st.face_shape && <ChipL>Cara {st.face_shape.name.toLowerCase()}</ChipL>}</div>
    </Frame>);
  if (G) cards.push(
    <Frame key="global" bg={2} eyebrow="Lectura global" title={<>Una cifra,<br /><em className="italic text-coral">con todo lo que la compone.</em></>} foot={["Es una lectura estadística de una foto", "facelab"]}>
      <div className="mt-6 font-display text-[220px] leading-[0.9] font-medium tracking-tighter">{G.score}<small className="mt-3 block text-[34px] font-medium tracking-normal text-muted-foreground" style={{ fontFamily: "var(--font-figtree)" }}>de 100 · armonía, rasgos, piel, simetría, proporción, perfil y edad</small></div>
      <div className="mt-8 flex flex-wrap gap-4">{Object.entries(G.components).slice(0, 6).map(([k, v]) => <ChipL key={k}>{COMP[k] || k} {Math.round(v)}</ChipL>)}</div>
    </Frame>);
  if (st.palette && st.season) cards.push(
    <Frame key="color" bg={1} eyebrow="Colorimetría" title={<>{st.season.name}<br /><em className="italic text-coral">es tu estación.</em></>} foot={[`Metales: ${st.palette.metals}`, `Contraste ${st.contrast?.level}`]}>
      <P>{st.season.summary}</P>
      <div className="mt-11 grid grid-cols-5 gap-x-5 gap-y-16">{st.palette.best.slice(0, 10).map((c) => <div key={c.hex} className="relative aspect-square rounded-[32px] border-2 border-black/5" style={{ background: c.hex }}><b className="absolute -bottom-10 right-0 left-0 text-center text-[20px] font-semibold text-ink-2">{c.name}</b></div>)}</div>
    </Frame>);
  if (strengths.length) cards.push(
    <Frame key="pros" eyebrow="Lo que juega a tu favor" title={<>Tus puntos<br /><em className="italic text-coral">fuertes.</em></>} foot={["Cada frase se apoya en una medida y un percentil", "facelab"]}>
      <ul className="mt-9">{strengths.slice(0, 4).map((x, i) => <li key={i} className="flex items-start gap-6 border-t-2 border-line py-7 text-[40px] leading-[1.25]"><span className="mt-4 size-[22px] shrink-0 rounded-full bg-coral" />{x}</li>)}</ul>
    </Frame>);
  const V = R.visualization;
  if (V?.after && face) cards.push(
    <Frame key="after" bg={2} eyebrow="Proyección" title={<>Antes<br /><em className="italic text-coral">y después de la rutina.</em></>} foot={["Ilustración, no promesa", "facelab"]}>
      <P>Cambios alcanzables sin cirugía: piel, cejas, pelo, descanso. Nivel {V.tier || ""}.</P>
      <div className="mt-10 grid grid-cols-2 gap-6">{[[face, "Antes"], [out(V.after), "Después"]].map(([src, l]) => <div key={l} className="relative aspect-[3/4] overflow-hidden rounded-[44px] bg-secondary"><Img src={src} /><b className="absolute bottom-6 left-6 rounded-full bg-ink/75 px-5 py-3 text-[26px] font-bold text-white">{l}</b></div>)}</div>
    </Frame>);
  const rd = st.renders || {}, look = (st.advice?.outfits || []).find((o) => rd[o.id]?.file);
  if (look) cards.push(
    <Frame key="look" bg={1} eyebrow="Tu look" title={<>{look.name}<br /><em className="italic text-coral">con tu paleta.</em></>} foot={[(look.pieces || []).slice(0, 2).join(" · "), "facelab"]}>
      <div className="relative mt-10 aspect-[4/5] overflow-hidden rounded-[44px] bg-secondary"><Img src={out(rd[look.id].file)} /><b className="absolute bottom-6 left-6 rounded-full bg-ink/75 px-5 py-3 text-[26px] font-bold text-white">{look.occasion || ""}</b></div>
    </Frame>);
  return cards;
}
