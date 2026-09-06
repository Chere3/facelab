"use client";
import { useEffect } from "react";
import { useReport, type Initial } from "@/hooks/useReport";
import { ForceMode, useMode } from "@/lib/mode";
import { out } from "@/lib/api";
import { Nav } from "@/components/site/Nav";
import { Footer } from "@/components/site/Footer";
import { Hero } from "@/components/report/Hero";
import { Global } from "@/components/report/Global";
import { Proportions } from "@/components/report/Proportions";
import { Symmetry } from "@/components/report/Symmetry";
import { Zone } from "@/components/report/Zone";
import { ProfileView } from "@/components/report/ProfileView";
import { Skin } from "@/components/report/Skin";
import { Protocol } from "@/components/report/Protocol";
import { Projection } from "@/components/report/Projection";
import { Style } from "@/components/report/Style";
import { Share } from "@/components/report/Share";
import { cn } from "@/lib/utils";

const SUBNAV = [["global", "Global"], ["proporciones", "Proporciones"], ["simetria", "Simetría"], ["ojos", "Ojos"], ["nariz", "Nariz"], ["perfil", "Perfil"], ["boca", "Boca"], ["inferior", "Mandíbula"], ["piel", "Piel"], ["rutina", "Rutina"], ["futuro", "Después"], ["estilo", "Estilo"], ["compartir", "Compartir"]];

export function ReportView({ stem, print, initial }: { stem: string; print: boolean; initial: Initial }) {
  const { report: R, status: S, missing, wake, stepState, stepDetail } = useReport(stem, initial);
  const { mode, setMode } = useMode();
  useEffect(() => { if (print) document.body.dataset.ready = S?.done ? "1" : "0"; }, [print, S]);

  return (
    <ForceMode value={print ? "sci" : null}>
      <Nav />
      <div className="no-print sticky top-[57px] z-20 glass border-b border-line">
        <div className="mx-auto flex max-w-[1240px] items-center gap-3 px-5 py-2 text-[12px] md:px-7">
          <nav className="no-scrollbar flex flex-1 gap-4 overflow-x-auto">{SUBNAV.map(([h, l]) => <a key={h} href={`#${h}`} className="font-medium whitespace-nowrap text-muted-foreground transition hover:text-ink">{l}</a>)}</nav>
          <span className="inline-flex shrink-0 gap-0.5 rounded-full bg-secondary p-0.5" title="Simple: solo lo esencial. Ciencia: cada medida, valor, percentil y norma.">
            {(["simple", "sci"] as const).map((m) => <button key={m} onClick={() => setMode(m)} className={cn("rounded-full px-3 py-1 text-[12px] font-semibold transition", mode === m ? "bg-paper text-ink shadow-soft" : "text-muted-foreground")}>{m === "simple" ? "Simple" : "Ciencia"}</button>)}
          </span>
        </div>
      </div>
      <Progress S={S} />

      <main className="mx-auto max-w-[1240px] px-5 md:px-7">
        {missing && !R ? (
          <div className="py-24 text-center"><h1 className="text-[40px] font-medium">Este informe no existe.</h1><p className="mt-2 text-muted-foreground">Comprueba el enlace o vuelve al <a className="underline" href="/feed">feed</a>.</p></div>
        ) : !R ? (
          <div className="grid gap-10 pt-10 md:grid-cols-[5fr_7fr]"><div className="sk aspect-square rounded-[40px]" /><div><div className="sk mb-4 h-3 w-40" /><div className="sk mb-3 h-14 w-4/5" /><div className="sk mb-6 h-14 w-3/5" /><h1 className="text-[28px] font-medium">Preparando tu informe…</h1><p className="text-muted-foreground">Detectando landmarks y calculando medidas. Unos segundos.</p></div></div>
        ) : (
          <>
            {print && <Cover R={R} />}
            <Hero R={R} status={S} stem={stem} onWake={wake} stepState={stepState} />
            <Global R={R} />
            <Proportions R={R} stepState={stepState} stepDetail={stepDetail} />
            <Symmetry R={R} stepState={stepState} stepDetail={stepDetail} />
            <Zone R={R} id="ojos" eyebrow="Zona 1" title={<>Ojos <em className="italic text-coral">y cejas.</em></>} photo="eyes_annot" lede="Forma, inclinación y separación de los ojos, y cómo las cejas los enmarcan." stepState={stepState} stepDetail={stepDetail} />
            <Zone R={R} id="nariz" eyebrow="Zona 2" title={<>La <em className="italic text-coral">nariz.</em></>} photo="nose_annot" lede="Anchura, altura e índice nasal frente a tu grupo. Los ángulos de perfil son estimados." stepState={stepState} stepDetail={stepDetail} />
            <ProfileView R={R} stepState={stepState} stepDetail={stepDetail} />
            <Zone R={R} id="boca" eyebrow="Zona 3" title={<>Boca <em className="italic text-coral">y labios.</em></>} photo="mouth_annot" lede="Anchura bucal, proporción de labios y comisuras." stepState={stepState} stepDetail={stepDetail} />
            <Zone R={R} id="inferior" eyebrow="Zona 4" title={<>Mandíbula <em className="italic text-coral">y mentón.</em></>} photo="lower_annot" lede="Anchura de mandíbula frente a pómulos, altura del mentón y del tercio inferior." stepState={stepState} stepDetail={stepDetail} />
            <Skin R={R} stepState={stepState} />
            <Protocol R={R} stepState={stepState} />
            <Projection R={R} status={S} stepState={stepState} />
            <Style R={R} stem={stem} stepState={stepState} stepDetail={stepDetail} onWake={wake} />
            <Share R={R} stem={stem} />
          </>
        )}
      </main>
      <Footer extra={R?.source ? <p className="mt-2 font-mono text-[11px]">JSON: {R.source}</p> : null} />
    </ForceMode>
  );
}

function Progress({ S }: { S: ReturnType<typeof useReport>["status"] }) {
  if (!S) return null;
  const cur = S.steps.find((s) => s.state === "running");
  const hasErr = !!S.error || S.steps.some((s) => s.state === "error");
  if (S.done && !hasErr) return null;
  return (
    <div className="no-print border-b border-line bg-paper">
      <div className="mx-auto flex max-w-[1240px] flex-wrap items-center gap-2 px-5 py-2 text-[12px] md:px-7">
        {S.steps.map((s) => (
          <span key={s.id} className={cn("inline-flex items-center gap-1.5 rounded-full border px-2.5 py-1", s.state === "running" ? "border-coral bg-coral-2 text-coral" : s.state === "done" ? "border-line text-ink" : s.state === "error" ? "border-destructive text-destructive" : "border-line text-muted-foreground", s.state === "skipped" && "opacity-50")}>
            <i className={cn("size-2 rounded-full", s.state === "running" ? "animate-pulse bg-coral" : s.state === "done" ? "bg-coral" : s.state === "error" ? "bg-destructive" : "bg-line-2")} />{s.label}{s.detail && s.state !== "pending" ? <span className="opacity-70"> · {s.detail}</span> : null}
          </span>
        ))}
        <span className="ml-auto text-muted-foreground">{cur ? `Generando: ${cur.label}` : S.done ? (S.error ? `Error: ${S.error}` : "Informe completo") : "En cola"}</span>
      </div>
    </div>
  );
}

/** Portada del PDF. */
function Cover({ R }: { R: NonNullable<ReturnType<typeof useReport>["report"]> }) {
  const s = R.scores || {};
  return (
    <div className="print-only" style={{ height: "262mm", breakAfter: "page", padding: "10mm 4mm 0" }}>
      <div className="flex items-center gap-2 font-display text-[18px] font-semibold"><span className="inline-block size-[18px] rounded-[30%]" style={{ background: "conic-gradient(from 200deg, var(--coral), var(--peach), var(--butter), var(--lavender), var(--coral))" }} />facelab</div>
      <div className="eyebrow" style={{ marginTop: "18mm" }}>Informe facial · {R.date}</div>
      <h1 className="text-[54px] leading-none font-medium" style={{ margin: "8mm 0", maxWidth: "14ch" }}>{R.person ? `${R.person}, ` : ""}tu cara, <em className="italic text-coral">medida y explicada.</em></h1>
      {R.assets?.face && <img src={out(R.assets.face)} alt="" style={{ width: "110mm", aspectRatio: "1", objectFit: "cover", borderRadius: 24, margin: "8mm 0" }} />}
      <div className="flex gap-10">{s.symmetry && <div><b className="text-[30px]">{s.symmetry.score}</b><small className="block text-muted-foreground">simetría</small></div>}{s.global?.composite && <div><b className="text-[30px]">{s.global.composite.score}</b><small className="block text-muted-foreground">lectura global</small></div>}{R.style?.season && <div><b className="text-[22px]">{R.style.season.name}</b><small className="block text-muted-foreground">estación de color</small></div>}{R.style?.face_shape && <div><b className="text-[22px]">{R.style.face_shape.name}</b><small className="block text-muted-foreground">forma de cara</small></div>}</div>
      <p className="mt-auto max-w-[90ch] text-[11px] text-muted-foreground" style={{ marginTop: "20mm" }}>Medidas geométricas sobre una foto, comparadas con caras de tu grupo en un dataset público. Sin notas de belleza. No es un documento clínico.</p>
    </div>
  );
}
