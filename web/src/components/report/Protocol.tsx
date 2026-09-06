"use client";
import type { Report } from "@/lib/types";
import { DIFF, EVIDENCE, TIER, costLabel, plainName, simplify } from "@/lib/plain";
import { useMode } from "@/lib/mode";
import { Sci, Simple } from "@/lib/mode";
import { Section, SectionHead } from "@/components/site/Section";
import { Chip } from "@/components/site/Chip";
import { Card, ErrBox } from "./bits";
import { cn } from "@/lib/utils";

const TIER_COLOR: Record<string, string> = { "glow-up": "var(--ink)", mejora: "var(--coral)", mantenimiento: "var(--lavender)" };

export function Protocol({ R, stepState }: { R: Report; stepState: (id: string) => string }) {
  const P = R.protocol, st = stepState("protocol");
  const { mode } = useMode();
  const I = P?.intensity || {};
  const tier = TIER[I.tier ?? ""];
  return (
    <Section id="rutina">
      <SectionHead eyebrow="Tu rutina" title={<>Qué hacer, <em className="italic text-coral">y en qué orden.</em></>} lede="Solo métodos no quirúrgicos con nivel de evidencia. Lo que ya está en su sitio no se toca." />
      {P?.phases?.length ? (
        <div className="mt-6 space-y-5">
          <Card className="border-l-4" >
            <div className="flex flex-wrap items-baseline gap-x-4 gap-y-1">
              <b className="font-display text-[26px] font-medium" style={{ color: TIER_COLOR[I.tier ?? ""] }}>{tier?.name ?? I.tier}</b>
              <span className="text-[13px] text-muted-foreground"><Simple as="span">{tier?.blurb}</Simple><Sci as="span">{I.rationale}{I.requested && I.requested !== I.computed ? ` · pedido por ti (calculado: ${I.computed})` : ""}</Sci></span>
            </div>
            <Sci>{!!I.drivers?.length && <div className="mt-2 flex flex-wrap gap-1.5">{I.drivers.map((d) => <Chip key={d} size="sm">{d}</Chip>)}</div>}</Sci>
          </Card>
          {P.target_look && <Letter title="Cómo te verás">{P.target_look}</Letter>}

          <ol className="relative space-y-6 border-l-2 border-line pl-6 md:pl-8">
            {P.phases.map((ph, i) => (
              <li key={i} className="relative">
                <span className="absolute -left-[33px] top-1 flex size-6 items-center justify-center rounded-full bg-coral text-[11px] font-bold text-white md:-left-[41px]">{i + 1}</span>
                <div className="eyebrow">{ph.weeks}</div>
                <h3 className="text-[20px] font-medium">{ph.name}</h3>
                <p className="mt-0.5 text-[13.5px] text-muted-foreground">{ph.goal}</p>
                <div className="mt-3 grid gap-3 md:grid-cols-2">
                  {(ph.actions || []).map((a, j) => (
                    <div key={j} className="card-soft p-4">
                      <div className="flex items-start justify-between gap-2"><b className="text-[15px] leading-tight">{a.name}</b>{a.evidence && <Chip size="sm" tone="accent" className="shrink-0">{EVIDENCE[a.evidence] ? EVIDENCE[a.evidence] : `evidencia ${a.evidence}`}</Chip>}</div>
                      {a.spec && <p className="mt-2 text-[13.5px] font-semibold text-ink-2">{a.spec}</p>}
                      <Simple>{a.why && <details className="mt-2 text-[13px] text-muted-foreground"><summary className="cursor-pointer font-semibold text-ink">¿Por qué?</summary><p className="mt-1">{a.why}</p></details>}</Simple>
                      <Sci>{a.why && <p className="mt-2 text-[13px] text-ink-2">{a.why}</p>}</Sci>
                      <div className="mt-3 flex flex-wrap gap-1.5">{[costLabel(a.cost), a.frequency, a.horizon, DIFF[a.difficulty ?? ""] ?? a.difficulty].filter(Boolean).map((t, k) => <Chip key={k} size="sm">{t}</Chip>)}</div>
                    </div>
                  ))}
                </div>
              </li>
            ))}
          </ol>

          <Sci>{!!P.expected_changes?.length && (
            <Card><h3 className="text-[16px] font-semibold">Qué debería moverse</h3>
              <table className="mt-2 w-full border-collapse text-[13px]"><thead><tr className="text-left text-[11px] text-muted-foreground"><th className="py-1 font-medium">Medida</th><th className="font-medium">Ahora</th><th className="font-medium">Objetivo</th><th className="font-medium">Cómo</th></tr></thead>
                <tbody>{P.expected_changes.map((e, i) => <tr key={i} className="border-t border-line align-top"><td className="py-1.5 pr-2">{plainName(e.measure.replace(/^skin\./, ""), R.catalog)}</td><td className="pr-2 font-mono text-[12px]">{e.now}</td><td className="pr-2 font-mono text-[12px]">{e.target}</td><td className="text-muted-foreground">{e.via}</td></tr>)}</tbody></table>
            </Card>)}</Sci>
          {!!P.not_recommended?.length && <Card><h3 className="text-[16px] font-semibold">No hace falta tocar</h3><ul className="mt-1 list-disc space-y-1 pl-5 text-[14px]">{P.not_recommended.map((x, i) => <li key={i}>{mode === "simple" ? simplify(x) : x}</li>)}</ul></Card>}
          {P.letter && <Letter title="Carta del equipo">{P.letter}</Letter>}
        </div>
      ) : st === "running" || st === "pending" ? (
        <div className="mt-6"><div className="grid gap-4 md:grid-cols-3">{[0, 1, 2].map((i) => <Card key={i}><div className="sk mb-2 h-3 w-10" /><div className="sk mb-3 h-5 w-3/5" />{[0, 1, 2].map((j) => <div key={j} className="sk my-2 h-3" />)}</Card>)}</div>
          <p className="mt-3 flex items-center gap-2 text-[12px] text-muted-foreground"><i className="size-2 animate-pulse rounded-full bg-coral" />{st === "running" ? "Claude está diseñando tu rutina a partir de la narrativa…" : "La rutina se genera tras la narrativa"}</p></div>
      ) : <ErrBox className="mt-5">La rutina falló. Usa «Rutina + imagen» para reintentar.</ErrBox>}
    </Section>
  );
}

export function Letter({ title, children, className }: { title: string; children: React.ReactNode; className?: string }) {
  return (
    <div className={cn("rounded-3xl bg-gradient-to-br from-peach-2 to-lavender-2/70 px-6 py-6 md:px-8", className)}>
      <div className="eyebrow mb-2">{title}</div>
      <div className="max-w-[70ch] font-display text-[18px] leading-relaxed md:text-[20px]" style={{ fontVariationSettings: '"opsz" 24, "SOFT" 80' }}>{children}</div>
    </div>
  );
}
