"use client";
import type { Report, Narr } from "@/lib/types";
import { pctOf, sciName } from "@/lib/plain";
import { Sci, useMode } from "@/lib/mode";
import { PctChip } from "@/components/charts/PercentileBar";
import { ErrBox, ProsCons, Skeleton } from "./bits";

export const NARR_KEY: Record<string, string> = { proporciones: "proporciones", ojos: "ojos_y_cejas", nariz: "nariz", boca: "boca_y_labios", inferior: "tercio_inferior", global: "global", perfil: "perfil" };

/** Sección narrativa: en simple solo puntos fuertes y a vigilar; en ciencia, resumen y hallazgos con percentil. */
export function Narrative({ R, k, state, detail }: { R: Report; k: string; state: string; detail?: string }) {
  const n: Narr | undefined = R.narrative?.[NARR_KEY[k] ?? k];
  const { mode } = useMode();
  if (n?.error) return <ErrBox>Esta sección no se pudo redactar: {n.error}. Usa «Solo narrativa» para reintentar.</ErrBox>;
  if (!n) {
    if (state === "error") return <ErrBox>La narrativa falló: {detail}. Usa «Solo narrativa».</ErrBox>;
    return <Skeleton label={state === "running" ? "Claude está redactando esta sección…" : "Narrativa pendiente"} lines={mode === "sci" ? 5 : 3} />;
  }
  return (
    <div className="space-y-4">
      <Sci>
        {n.summary && <p className="max-w-[70ch] border-l-[3px] border-coral pl-4 text-[15.5px] leading-relaxed">{n.summary}</p>}
        {!!n.findings?.length && (
          <div className="mt-4 grid gap-2.5 sm:grid-cols-2">
            {n.findings.map((f, i) => (
              <div key={i} className="rounded-2xl border border-line bg-paper px-3.5 py-3">
                <div className="mb-1 flex items-center justify-between gap-2"><b className="text-[13px]">{sciName(f.measure, R.catalog)}</b><PctChip p={pctOf(R, f.measure)} /></div>
                <p className="text-[13px] leading-snug text-ink-2">{f.statement}</p>
              </div>
            ))}
          </div>
        )}
      </Sci>
      <ProsCons pros={n.strengths || []} cons={n.watch || []} />
    </div>
  );
}
