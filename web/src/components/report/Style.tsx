"use client";
import { useState } from "react";
import type { Report, Look, Render } from "@/lib/types";
import { out, regen } from "@/lib/api";
import { fmt } from "@/lib/plain";
import { Sci, Simple } from "@/lib/mode";
import { HBars } from "@/components/charts/Bars";
import { Section, SectionHead } from "@/components/site/Section";
import { Chip } from "@/components/site/Chip";
import { Button } from "@/components/ui/button";
import { Card, Cap, Empty, ErrBox, Photo, Skeleton } from "./bits";
import { Letter } from "./Protocol";
import { cn } from "@/lib/utils";

const EX: Record<string, string> = { feminine: "más femenino", masculine: "más masculino", neutral: "tu expresión" };

export function Style({ R, stem, stepState, stepDetail, onWake }: { R: Report; stem: string; stepState: (id: string) => string; stepDetail: (id: string) => string; onWake: () => void }) {
  const st = R.style, ss = stepState("style"), looks = stepState("looks");
  const [shirt, setShirt] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);
  const go = async (steps: string[], look_ids?: string[]) => { setBusy(true); try { await regen(stem, steps, look_ids ? { look_ids } : {}); onWake(); } finally { setBusy(false); } };

  let inner: React.ReactNode;
  if (st?.season && st.palette) {
    const C = st.colors || {}, P = st.palette, A = st.advice || {};
    const items = st.shirts?.items || [];
    const cur = items.find((x) => x.file === shirt) || items[0];
    inner = (
      <div className="mt-6 space-y-6">
        {/* estación: tarjeta protagonista con la paleta como fondo */}
        <div className="grid gap-4 md:grid-cols-[minmax(0,7fr)_minmax(0,5fr)]">
          <div className="relative overflow-hidden rounded-[32px] p-6 text-white md:p-8" style={{ background: `linear-gradient(120deg, ${P.best.slice(0, 4).map((c) => c.hex).join(", ")})` }}>
            <div className="absolute inset-0 bg-black/15" />
            <div className="relative">
              <div className="text-[11px] font-bold tracking-[0.16em] uppercase opacity-90">Tu estación de color</div>
              <h3 className="mt-1 text-[clamp(30px,4vw,48px)] font-medium leading-none">{st.season.name}</h3>
              <p className="mt-3 max-w-[48ch] text-[15px] opacity-95">{st.season.summary}</p>
              <div className="mt-4 flex flex-wrap gap-2">{P.best.map((c) => <span key={c.hex} className="flex items-center gap-1.5 rounded-full bg-white/20 px-2.5 py-1 text-[12px] font-semibold backdrop-blur"><i className="size-3 rounded-full border border-white/50" style={{ background: c.hex }} />{c.name}</span>)}</div>
              <Sci><ul className="mt-4 list-disc space-y-0.5 pl-5 text-[13px] opacity-95">{(st.season.why || []).map((w) => <li key={w}>{w}</li>)}</ul><p className="mt-2 text-[12px] opacity-85">Segunda opción: {st.season.secondary} (margen {st.season.margin}). Contraste {st.contrast?.level}: {st.contrast?.rule}</p></Sci>
            </div>
          </div>
          <div className="space-y-4">
            <Card>
              <div className="grid grid-cols-3 gap-2">
                {(["skin", "hair", "eyes"] as const).map((k) => { const c = C[k]; const label = { skin: "Piel", hair: "Pelo", eyes: "Ojos" }[k]; return (
                  <div key={k} className="text-center"><span className="mx-auto block size-14 rounded-2xl border border-white/10" style={{ background: c?.hex || "var(--secondary)" }} /><b className="mt-1.5 block text-[13px]">{label}</b><small className="block text-[11px] leading-tight text-muted-foreground">{c ? (k === "skin" ? `${c.depth}, subtono ${c.undertone}` : c.label) : "no visible"}</small><Sci><small className="block font-mono text-[10px] text-muted-foreground">{c?.hex} · L* {c?.L}</small></Sci></div>
                ); })}
              </div>
            </Card>
            <Card>
              <div className="flex items-center justify-between"><div><div className="eyebrow">Forma de cara</div><b className="font-display text-[24px] font-medium">{st.face_shape?.name}</b></div><Chip tone="lavender">Contraste {st.contrast?.level}</Chip></div>
              <Sci><Cap>{st.face_shape?.note}. Índice facial {fmt(st.face_shape?.inputs?.facial_index)}, mandíbula/pómulos {fmt(st.face_shape?.inputs?.jaw_to_cheek, 3)}.{st.hair?.visible ? ` Pelo actual: ${st.hair.length}.` : ""}</Cap>
                {!!st.season.ranking?.length && <div className="mt-3"><HBars data={st.season.ranking.slice(0, 4).map((r) => ({ k: r.name, v: +r.score.toFixed(2) }))} highlight={st.season.name} height={130} format={(v) => `${v.toFixed(2)}`} /><Cap className="mt-0">Distancia a cada estación (menos es más cercana).</Cap></div>}</Sci>
            </Card>
          </div>
        </div>

        <div className="grid gap-4 md:grid-cols-3">
          <Swatches title="Neutros base" list={P.neutrals} />
          <Swatches title="Evitar junto a la cara" list={P.avoid} />
          <Card><div className="eyebrow">Metales y estampados</div><p className="mt-1 text-[14px]"><b>Metales:</b> {P.metals}</p><p className="mt-1 text-[13px] text-muted-foreground">{P.patterns}</p>{!!P.makeup?.length && <p className="mt-2 text-[13px]"><b>Maquillaje:</b> {P.makeup.join(" · ")}</p>}</Card>
        </div>

        {items.length > 0 && cur && (
          <div>
            <h3 className="text-[22px] font-medium">La misma foto, <span className="gradient-text">con distintas camisas.</span></h3>
            <Cap className="mt-0">{st.shirts?.mode === "recolor" ? "Se recolorea la prenda real de tu foto conservando pliegues y sombras." : "No se ve ropa en la foto: se simula con una tela bajo el mentón."} Toca un color.</Cap>
            <div className="mt-4 grid gap-5 md:grid-cols-[minmax(0,4fr)_minmax(0,8fr)]">
              <Photo src={out(cur.file)} ratio="auto" fit="contain" className="max-w-[360px]" />
              <div className="space-y-3">
                {([["best", "Mejores"], ["neutral", "Neutros"], ["avoid", "A evitar, para comparar"]] as const).map(([g, l]) => (
                  <div key={g}><div className="eyebrow mb-1.5">{l}</div><div className="flex flex-wrap gap-2">{items.filter((x) => x.group === g).map((x) => (
                    <button key={x.file} onClick={() => setShirt(x.file)} className={cn("flex items-center gap-1.5 rounded-full border bg-paper py-1 pr-3 pl-1.5 text-[12px] font-semibold transition", cur.file === x.file ? "border-coral ring-2 ring-coral-2" : "border-line hover:border-line-2")}><i className="size-4 rounded-full border border-white/10" style={{ background: x.hex }} />{x.name}</button>
                  ))}</div></div>
                ))}
              </div>
            </div>
          </div>
        )}

        {A.summary ? (
          <>
            <Letter title="Tu colorimetría, en corto">{A.summary} <Sci as="span">{A.color_story}</Sci></Letter>
            {!!A.wardrobe?.length && (
              <div><h3 className="text-[22px] font-medium">Armario</h3>
                <div className="mt-3 grid gap-3 sm:grid-cols-2 md:grid-cols-3">{A.wardrobe.map((w) => <Card key={w.category} className="p-4"><h4 className="text-[11px] font-bold tracking-[0.12em] text-muted-foreground uppercase">{w.category}</h4><ul className="mt-1.5 space-y-1 text-[13px]">{(w.picks || []).map((x, i) => <li key={i} className="flex gap-2"><span className="mt-2 size-1.5 shrink-0 rounded-full bg-coral" />{x}</li>)}</ul>{!!w.avoid?.length && <p className="mt-2 text-[12px] text-destructive">Evitar: {w.avoid.join("; ")}</p>}</Card>)}</div></div>
            )}
            <LookGrid title="Seis looks, cuatro ocasiones, dos expresiones" items={A.outfits} renders={st.renders} state={looks} onRender={(id) => go(["looks"], [id])} />
            <LookGrid title="Cortes de pelo" items={A.haircuts} renders={st.renders} state={looks} onRender={(id) => go(["looks"], [id])} />
            <LookGrid title="Barba, cejas y maquillaje" items={A.grooming} renders={st.renders} state={looks} onRender={(id) => go(["looks"], [id])} />
            {(!!A.hair_color?.length || !!A.avoid?.length) && (
              <div className="grid gap-4 md:grid-cols-2">
                {!!A.hair_color?.length && <Card><h3 className="text-[16px] font-semibold">Color de pelo</h3><ul className="mt-1 list-disc space-y-1 pl-5 text-[13.5px]">{A.hair_color.map((x, i) => <li key={i}>{x}</li>)}</ul></Card>}
                {!!A.avoid?.length && <Card><h3 className="text-[16px] font-semibold">Qué no te favorece</h3><ul className="mt-1 list-disc space-y-1 pl-5 text-[13.5px]">{A.avoid.map((x, i) => <li key={i}>{x}</li>)}</ul></Card>}
              </div>
            )}
          </>
        ) : ss === "running" ? <Skeleton label="Claude está redactando la asesoría de estilo (armario, looks, cortes)…" lines={6} /> : ss === "error" ? <ErrBox>La asesoría falló: {stepDetail("style")}</ErrBox> : null}

        <div className="no-print flex flex-wrap items-center gap-2">
          <Button variant="outline" className="rounded-full" disabled={busy} onClick={() => go(["style"])}>Recalcular colorimetría y asesoría</Button>
          <Button className="rounded-full" disabled={busy || looks === "running"} onClick={() => go(["looks"])}>{looks === "running" ? `Renderizando… ${stepDetail("looks")}` : "Renderizar todos los looks"}</Button>
          {A.summary && <Cap className="mt-0 basis-full">Los renders parten de tu foto de busto y cambian solo ropa, accesorios, pelo o grooming. Unos 1–2 min por imagen, tres a la vez.</Cap>}
        </div>
      </div>
    );
  } else if (ss === "running") inner = <div className="mt-6 space-y-4"><div className="sk h-56 rounded-[32px]" /><Skeleton label="Midiendo piel, pelo y ojos, paleta y forma de cara…" lines={4} /></div>;
  else if (ss === "error") inner = <div className="mt-6 space-y-3"><ErrBox>La colorimetría falló: {stepDetail("style")}</ErrBox><Button variant="outline" className="rounded-full" onClick={() => go(["style"])}>Reintentar</Button></div>;
  else inner = <div className="mt-6 space-y-3"><Empty>Este informe aún no tiene colorimetría.</Empty><Button className="rounded-full" onClick={() => go(["style"])}>Calcular colorimetría y estilo</Button></div>;

  return (
    <Section id="estilo">
      <SectionHead eyebrow="Colorimetría y estilo" title={<>Qué colores, cortes y prendas <span className="gradient-text">te favorecen.</span></>} lede={<><Simple>Tus colores medidos en la foto, tu estación, tu forma de cara y looks sobre tu propia imagen.</Simple><Sci>Piel, pelo y ojos medidos en CIELAB, estación de color con paleta, forma de cara y looks renderizados. Orientativo: la luz y el balance de blancos mueven el subtono.</Sci></>} />
      {inner}
    </Section>
  );
}

function Swatches({ title, list }: { title: string; list: { hex: string; name: string }[] }) {
  return <Card><div className="eyebrow">{title}</div><div className="mt-2 flex flex-wrap gap-2">{list.map((c) => <div key={c.hex} className="w-14 text-center text-[10px] leading-tight text-muted-foreground"><i className="mb-1 block h-9 rounded-xl border border-white/10" style={{ background: c.hex }} />{c.name}</div>)}</div></Card>;
}

function LookGrid({ title, items, renders = {}, state, onRender }: { title: string; items?: Look[]; renders?: Record<string, Render>; state: string; onRender: (id: string) => void }) {
  if (!items?.length) return null;
  return (
    <div>
      <h3 className="text-[22px] font-medium">{title}</h3>
      <div className="mt-3 grid gap-4 sm:grid-cols-2 md:grid-cols-3">
        {items.map((o) => { const r = renders[o.id]; return (
          <div key={o.id} className="card-soft flex flex-col overflow-hidden p-0">
            {r?.file ? <Photo src={out(r.file, r.ts)} className="rounded-none" /> : state === "running" ? <div className="sk aspect-square rounded-none" /> : r?.error ? <div className="flex aspect-square items-center justify-center bg-secondary p-4 text-center text-[12px] text-destructive">Render fallido: {r.error.slice(0, 140)}</div> : <div className="no-print flex aspect-square items-center justify-center bg-secondary"><Button variant="outline" className="rounded-full" onClick={() => onRender(o.id)}>Renderizar</Button></div>}
            <div className="p-4 text-[13px]">
              <span className={cn("text-[11px] font-semibold tracking-wider uppercase", o.expression === "feminine" ? "text-[#c2418a]" : o.expression === "masculine" ? "text-sky" : "text-muted-foreground")}>{EX[o.expression ?? ""]}{o.occasion ? ` · ${o.occasion}` : ""}</span>
              <h4 className="mt-0.5 text-[16px] font-semibold">{o.name || o.id}</h4>
              {o.description && <p className="mt-1 text-ink-2">{o.description}</p>}
              {!!o.pieces?.length && <ul className="mt-1.5 space-y-0.5 text-ink-2">{o.pieces.map((x, i) => <li key={i} className="flex gap-2"><span className="mt-2 size-1 shrink-0 rounded-full bg-ink-2" />{x}</li>)}</ul>}
              {!!o.colors?.length && <div className="mt-2 flex gap-1.5">{o.colors.map((c) => <i key={c} className="size-5 rounded-md border border-white/10" style={{ background: c }} />)}</div>}
              {o.accessories?.length ? <p className="mt-1.5"><b>Accesorios:</b> {o.accessories.join(", ")}</p> : null}
              {o.grooming && <p className="mt-1"><b>Grooming:</b> {o.grooming}</p>}
              <Sci>{o.maintenance && <p className="mt-1"><b>Mantenimiento:</b> {o.maintenance}</p>}{o.why && <Cap>{o.why}</Cap>}</Sci>
              {r?.file && state !== "running" && <Button variant="outline" size="sm" className="no-print mt-3 rounded-full" onClick={() => onRender(o.id)}>Re-renderizar</Button>}
            </div>
          </div>
        ); })}
      </div>
    </div>
  );
}
