"use client";
import { useState } from "react";
import type { Report, Status } from "@/lib/types";
import { out } from "@/lib/api";
import { Sci } from "@/lib/mode";
import { BeforeAfter } from "@/components/charts/BeforeAfter";
import { Section, SectionHead } from "@/components/site/Section";
import { Cap, ErrBox } from "./bits";
import { cn } from "@/lib/utils";

export function Projection({ R, status, stepState }: { R: Report; status: Status | null; stepState: (id: string) => string }) {
  const V = R.visualization, st = stepState("visualize");
  const [which, setWhich] = useState<"3m" | "12m">("12m");
  const after = which === "3m" && V?.after_3m ? V.after_3m : V?.after;
  const detail = status?.steps.find((s) => s.id === "visualize")?.detail || "";
  return (
    <Section id="futuro">
      <SectionHead eyebrow="Visualización" title={<>Tu cara <em className="italic text-coral">después de la rutina.</em></>} lede="Generada a partir de tu foto y de las acciones del plan. Cambios sutiles y alcanzables sin cirugía. Es una ilustración, no una promesa." />
      {V?.after && R.assets?.face ? (
        <div className="mt-6 max-w-[640px]">
          {V.after_3m && <div className="no-print mb-3 inline-flex gap-1 rounded-full bg-secondary p-1">{(["3m", "12m"] as const).map((w) => <button key={w} onClick={() => setWhich(w)} className={cn("rounded-full px-4 py-1.5 text-[13px] font-semibold transition", which === w ? "bg-paper text-ink shadow-soft" : "text-muted-foreground")}>{w === "3m" ? "3 meses" : "12 meses · look objetivo"}</button>)}</div>}
          <BeforeAfter before={out(R.assets.face)} after={out(after)} labels={["Antes", "Proyección"]} />
          <Cap>Arrastra para comparar. Nivel {V.tier}. <Sci as="span">Modelo {V.model} vía Codex. Basada en el look objetivo y en tus estadísticas: {(V.edits || []).join(" · ")}.</Sci></Cap>
        </div>
      ) : st === "running" || st === "pending" ? <div className="mt-6 max-w-[640px]"><div className="sk aspect-square rounded-3xl" /><Cap className="flex items-center gap-2"><i className="size-2 animate-pulse rounded-full bg-coral" />{st === "running" ? "Codex está generando la proyección (1–2 min)…" : "Se genera tras la rutina"}</Cap></div>
      : <ErrBox className="mt-5">La visualización falló: {detail}. Usa «Rutina + imagen».</ErrBox>}
    </Section>
  );
}
