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

  const ModeToggle = (
    <span className="inline-flex shrink-0 gap-0.5 rounded-full bg-surface-3 p-0.5" title="Simple: solo lo esencial. Ciencia: cada medida, valor, percentil y norma.">
      {(["simple", "sci"] as const).map((m) => <button key={m} onClick={() => setMode(m)} className={cn("rounded-full px-3 py-1 text-[12px] font-semibold transition", mode === m ? "btn-glow" : "text-muted-foreground hover:text-ink")}>{m === "simple" ? "Simple" : "Ciencia"}</button>)}
    </span>
  );

  return (
    <ForceMode value={print ? "sci" : null}>
      <div className="bg-blobs min-h-screen">
        <Nav />
        {/* móvil: subnavegación horizontal */}
        <div className="no-print sticky top-[57px] z-20 glass border-b border-line lg:hidden">
          <div className="mx-auto flex max-w-[1400px] items-center gap-3 px-5 py-2 text-[12px]">
            <nav className="no-scrollbar flex flex-1 gap-4 overflow-x-auto">{SUBNAV.map(([h, l]) => <a key={h} href={`#${h}`} className="font-medium whitespace-nowrap text-muted-foreground transition hover:text-ink">{l}</a>)}</nav>
            {ModeToggle}
          </div>
        </div>

        <div className="mx-auto max-w-[1400px] px-5 pb-10 md:px-7 lg:grid lg:grid-cols-[210px_minmax(0,1fr)] lg:gap-7">
          {/* escritorio: barra lateral fija con secciones, modo y progreso */}
          <aside className="no-print sticky top-[76px] hidden self-start lg:block">
            <div className="mb-3">{ModeToggle}</div>
            <nav className="flex flex-col gap-0.5 text-[13px]">{SUBNAV.map(([h, l]) => <a key={h} href={`#${h}`} className="rounded-lg px-2.5 py-1.5 font-medium text-muted-foreground transition hover:bg-surface-2 hover:text-ink">{l}</a>)}</nav>
            <Progress S={S} compact />
          </aside>

          <main className="min-w-0">
            <Progress S={S} />
            {missing && !R ? (
              <div className="py-24 text-center"><h1 className="text-[40px]">Este informe no existe.</h1><p className="mt-2 text-muted-foreground">Comprueba el enlace o vuelve al <a className="underline" href="/feed">feed</a>.</p></div>
            ) : !R ? (
              <div className="panel mt-6 grid gap-8 p-6 md:grid-cols-[4fr_8fr]"><div className="sk aspect-square rounded-3xl" /><div><div className="sk mb-4 h-3 w-40" /><div className="sk mb-3 h-12 w-4/5" /><div className="sk mb-6 h-12 w-3/5" /><h1 className="text-[26px]">Preparando tu informe…</h1><p className="text-muted-foreground">Detectando landmarks y calculando medidas. Unos segundos.</p></div></div>
            ) : (
              <div className="flex flex-col gap-5 pt-5">
                {print && <Cover R={R} />}
                <Hero R={R} status={S} stem={stem} onWake={wake} stepState={stepState} />
                <Global R={R} />
                <Proportions R={R} stepState={stepState} stepDetail={stepDetail} />
                <Symmetry R={R} stepState={stepState} stepDetail={stepDetail} />
                <Zone R={R} id="ojos" eyebrow="Zona 1" title={<>Ojos <span className="gradient-text">y cejas</span></>} photo="eyes_annot" lede="Forma, inclinación y separación de los ojos, y cómo las cejas los enmarcan." stepState={stepState} stepDetail={stepDetail} />
                <Zone R={R} id="nariz" eyebrow="Zona 2" title={<>La <span className="gradient-text">nariz</span></>} photo="nose_annot" lede="Anchura, altura e índice nasal frente a tu grupo. Los ángulos de perfil son estimados." stepState={stepState} stepDetail={stepDetail} />
                <ProfileView R={R} stepState={stepState} stepDetail={stepDetail} />
                <Zone R={R} id="boca" eyebrow="Zona 3" title={<>Boca <span className="gradient-text">y labios</span></>} photo="mouth_annot" lede="Anchura bucal, proporción de labios y comisuras." stepState={stepState} stepDetail={stepDetail} />
                <Zone R={R} id="inferior" eyebrow="Zona 4" title={<>Mandíbula <span className="gradient-text">y mentón</span></>} photo="lower_annot" lede="Anchura de mandíbula frente a pómulos, altura del mentón y del tercio inferior." stepState={stepState} stepDetail={stepDetail} />
                <Skin R={R} stepState={stepState} />
                <Protocol R={R} stepState={stepState} />
                <Projection R={R} status={S} stepState={stepState} />
                <Style R={R} stem={stem} stepState={stepState} stepDetail={stepDetail} onWake={wake} />
                <Share R={R} stem={stem} />
              </div>
            )}
          </main>
        </div>
        <Footer extra={R?.source ? <p className="mt-2 font-mono text-[11px]">JSON: {R.source}</p> : null} />
      </div>
    </ForceMode>
  );
}

function Progress({ S, compact }: { S: ReturnType<typeof useReport>["status"]; compact?: boolean }) {
  if (!S) return null;
  const cur = S.steps.find((s) => s.state === "running");
  const hasErr = !!S.error || S.steps.some((s) => s.state === "error");
  if (S.done && !hasErr) return null;
  const dot = (st: string) => cn("size-2 shrink-0 rounded-full", st === "running" ? "animate-pulse bg-coral" : st === "done" ? "bg-mint" : st === "error" ? "bg-destructive" : "bg-line-2");
  if (compact) return (
    <div className="mt-5 border-t border-line pt-4 text-[12px]">
      <div className="mb-2 font-semibold text-ink">{cur ? `Generando: ${cur.label}` : S.done ? (S.error ? "Con errores" : "Completo") : "En cola"}</div>
      <ul className="space-y-1.5">{S.steps.map((s) => <li key={s.id} className={cn("flex items-center gap-2 text-muted-foreground", s.state === "running" && "text-coral", s.state === "done" && "text-ink-2", s.state === "skipped" && "opacity-50")}><i className={dot(s.state)} /><span className="truncate">{s.label.replace(/ \(.*\)/, "")}</span></li>)}</ul>
    </div>
  );
  return (
    <div className="no-print mt-4 flex flex-wrap items-center gap-2 rounded-2xl border border-line bg-surface p-3 text-[12px] lg:hidden">
      {S.steps.map((s) => <span key={s.id} className={cn("inline-flex items-center gap-1.5 rounded-full border border-line px-2.5 py-1", s.state === "running" ? "text-coral" : s.state === "done" ? "text-ink" : s.state === "error" ? "text-destructive" : "text-muted-foreground", s.state === "skipped" && "opacity-50")}><i className={dot(s.state)} />{s.label}</span>)}
      <span className="ml-auto text-muted-foreground">{cur ? `Generando: ${cur.label}` : S.done ? (S.error ? `Error: ${S.error}` : "Informe completo") : "En cola"}</span>
    </div>
  );
}

/** Portada del PDF. */
function Cover({ R }: { R: NonNullable<ReturnType<typeof useReport>["report"]> }) {
  const s = R.scores || {};
  return (
    <div className="print-only" style={{ height: "262mm", breakAfter: "page", padding: "10mm 4mm 0" }}>
      <div className="flex items-center gap-2 font-display text-[18px] font-semibold"><span className="inline-block size-[18px] rounded-[30%]" style={{ background: "conic-gradient(from 200deg, #ff5c7a, #ffb27a, #f0b429, #8f6ff0, #ff5c7a)" }} />facelab</div>
      <div className="eyebrow" style={{ marginTop: "18mm" }}>Informe facial · {R.date}</div>
      <h1 className="text-[54px] leading-none" style={{ margin: "8mm 0", maxWidth: "14ch" }}>{R.person ? `${R.person}, ` : ""}tu cara, medida y explicada.</h1>
      {R.assets?.face && <img src={out(R.assets.face)} alt="" style={{ width: "110mm", aspectRatio: "1", objectFit: "cover", borderRadius: 24, margin: "8mm 0" }} />}
      <div className="flex gap-10">{s.symmetry && <div><b className="text-[30px]">{s.symmetry.score}</b><small className="block text-muted-foreground">simetría</small></div>}{s.global?.composite && <div><b className="text-[30px]">{s.global.composite.score}</b><small className="block text-muted-foreground">lectura global</small></div>}{R.style?.season && <div><b className="text-[22px]">{R.style.season.name}</b><small className="block text-muted-foreground">estación de color</small></div>}{R.style?.face_shape && <div><b className="text-[22px]">{R.style.face_shape.name}</b><small className="block text-muted-foreground">forma de cara</small></div>}</div>
      <p className="mt-auto max-w-[90ch] text-[11px] text-muted-foreground" style={{ marginTop: "20mm" }}>Medidas geométricas sobre una foto, comparadas con caras de tu grupo en un dataset público. Sin notas de belleza. No es un documento clínico.</p>
    </div>
  );
}
