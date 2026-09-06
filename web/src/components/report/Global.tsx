"use client";
import type { Report } from "@/lib/types";
import { COMP, COMP_SCI, fmt } from "@/lib/plain";
import { Sci, Simple } from "@/lib/mode";
import { Ring } from "@/components/charts/Ring";
import { RadarScore } from "@/components/charts/RadarScore";
import { Section, SectionHead } from "@/components/site/Section";
import { Card, Cap, WarnBox } from "./bits";

export function Global({ R }: { R: Report }) {
  const G = R.scores?.global; if (!G?.composite) return null;
  const C = G.composite, M = G.model;
  const entries = Object.entries(C.components);
  const best = [...entries].sort((a, b) => b[1] - a[1])[0];
  const worst = [...entries].sort((a, b) => a[1] - b[1])[0];
  return (
    <Section id="global">
      <SectionHead eyebrow="Lectura global" title={<>Una cifra, <em className="italic text-coral">con todo lo que la compone.</em></>}
        lede={<Simple>Siete marcos medidos, uno al lado del otro. No es una nota: te dice qué pesa más en tu caso.</Simple>} />
      <div className="mt-6 grid gap-5 md:grid-cols-2">
        <Card>
          <div className="flex items-center gap-5">
            <Ring value={C.score} size={132} stroke={11} color="var(--ink)" label="de 100" />
            <div>
              <div className="eyebrow">Tu lectura</div>
              <p className="mt-1 text-[15px] leading-snug">Lo que más suma: <b>{COMP[best[0]] || best[0]}</b>. Donde hay más margen: <b>{COMP[worst[0]] || worst[0]}</b>.</p>
            </div>
          </div>
          <RadarScore data={entries.map(([k, v]) => ({ k: COMP[k] || k, v: Math.round(v) }))} className="mx-auto mt-2 aspect-square w-full max-w-[320px]" />
          <Sci>
            <table className="mt-2 w-full border-collapse text-[13px]">
              <tbody>{entries.map(([k, v]) => (
                <tr key={k} className="border-t border-line"><td className="py-1.5 pr-2">{COMP_SCI[k] || k}<div className="text-[11px] text-muted-foreground">{C.notes?.[k]}</div></td><td className="tabular text-right font-mono">{fmt(v, 1)}</td><td className="tabular text-right font-mono text-muted-foreground">×{Math.round((C.weights?.[k] ?? 0) * 100)}%</td></tr>
              ))}</tbody>
            </table>
            {!!C.missing?.length && <Cap>Sin datos para: {C.missing.map((k) => COMP_SCI[k] || k).join(", ")} (los pesos se reparten entre el resto).</Cap>}
            <Cap>{C.method}</Cap>
          </Sci>
        </Card>
        <div className="space-y-4">
          {M ? (
            <Card>
              <div className="flex items-center gap-5">
                <Ring value={M.percentile_in_group} size={96} stroke={9} color="var(--lavender)" label="percentil" />
                <div><b className="font-display text-[34px] leading-none font-medium">{M.predicted_rating}<span className="text-[16px] text-muted-foreground"> / 10</span></b>
                  <Cap className="mt-1"><Simple>Lo que un modelo entrenado con valoraciones de personas reales prevé para tu cara. Es estadística, no un veredicto.</Simple><Sci>Valoración humana prevista · percentil {Math.round(M.percentile_in_group)} en {M.group} (n={M.n_group}, media {M.group_human_mean})</Sci></Cap></div>
              </div>
              <Sci className="mt-3 text-[13.5px]">
                <p>{M.note}</p>
                <dl className="mt-2 grid grid-cols-[auto_1fr] gap-x-4 gap-y-1 text-[13px]"><dt className="text-muted-foreground">Entrenado con</dt><dd>{M.n_train} caras de MEBeauty, {M.scale}</dd><dt className="text-muted-foreground">Fiabilidad (CV)</dt><dd>R² {M.cv_r2} · r {M.cv_r}</dd><dt className="text-muted-foreground">Entradas</dt><dd>32 ratios y ángulos, 25 componentes de forma, 5 métricas de piel, sexo. La ascendencia no entra para no codificar sesgos.</dd></dl>
              </Sci>
            </Card>
          ) : <Card><p className="text-muted-foreground">Modelo no disponible</p></Card>}
          <WarnBox>Una cifra de atractivo es una lectura estadística de una foto, no un juicio sobre ti. Cambia con la luz, la expresión y quien mira. Úsala para ver qué pesa más en tu caso, no como veredicto.</WarnBox>
        </div>
      </div>
    </Section>
  );
}
