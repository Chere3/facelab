"use client";
import type { Report } from "@/lib/types";
import { out } from "@/lib/api";
import { band, bandShort, fmt } from "@/lib/plain";
import { Sci, Simple } from "@/lib/mode";
import { Ring } from "@/components/charts/Ring";
import { PercentileBar } from "@/components/charts/PercentileBar";
import { Section, SectionHead } from "@/components/site/Section";
import { Chip } from "@/components/site/Chip";
import { Card, Cap, Empty, Photo } from "./bits";

const ITEMS: [string, string, string, string, string][] = [
  ["redness_pct", "redness", "Rojez", "%", "piel con enrojecimiento sobre tu tono base"],
  ["spots_pct", "spots", "Manchas", "%", "piel más oscura que su entorno (pigmentación, pliegues)"],
  ["texture_index", "texture", "Textura y poros", "", "rugosidad local; más alto = más textura visible"],
  ["shine_pct", "shine", "Brillo", "%", "piel con brillo especular (grasa)"],
];

export function Skin({ R, stepState }: { R: Report; stepState: (id: string) => string }) {
  const k = R.skin, st = stepState("visual");
  const P = (k?.percentiles || {}) as Record<string, { percentile: number; group_mean?: number }>;
  const pctLabel = (p?: number) => { const b = band(p); return !b ? "sin normas" : b === "mid" ? "como tu grupo" : (b === "lo" || b === "lo2") ? `menos que tu grupo` : `más que tu grupo`; };
  return (
    <Section id="piel">
      <SectionHead eyebrow="Piel" title={<>Mapas <span className="gradient-text">de piel.</span></>} lede={<><Simple>Cuatro mapas de calor sobre tu piel. Cuanto más bajo, mejor: aquí «menos que tu grupo» es buena noticia.</Simple><Sci>Rojez, manchas, textura y brillo con percentiles frente a fotos de tu grupo con luz variada, así que son orientativos.</Sci></>} />
      {k?.maps ? (
        <>
          <div className="mt-6 grid grid-cols-2 gap-4 md:grid-cols-4">
            {ITEMS.map(([key, map, label, unit, desc]) => { const p = P[key]?.percentile; const b = band(p); return (
              <Card key={key} className="p-3">
                <Photo src={out(k.maps?.[map])} className="rounded-2xl" />
                <div className="mt-3 flex items-center gap-3">
                  <Ring value={p} size={54} stroke={6} color={b === "hi" ? "var(--apricot)" : b === "lo" ? "var(--sage)" : "var(--coral)"}><span className="text-[11px] font-bold">{p == null ? "–" : `p${Math.round(p)}`}</span></Ring>
                  <div className="min-w-0"><b className="block text-[14px] leading-tight">{label}</b><Chip size="sm" tone={b === "hi" ? "warn" : b === "lo" ? "ok" : "neutral"} className="mt-1">{pctLabel(p)}</Chip></div>
                </div>
                <Sci><b className="tabular mt-2 block text-[18px]">{fmt(k[key as keyof typeof k] as number)}{unit}</b><PercentileBar p={p} className="mt-1" /><Cap>{desc}</Cap></Sci>
              </Card>
            ); })}
          </div>
          <Sci className="mt-4 grid gap-4 md:grid-cols-2">
            <Card><dl className="grid grid-cols-[auto_1fr] gap-x-4 gap-y-1.5 text-[13.5px]"><dt className="text-muted-foreground">Uniformidad de tono</dt><dd className="tabular">{k.tone_unevenness} {P.tone_unevenness && <Chip size="sm">{bandShort[band(P.tone_unevenness.percentile)!]} · p{Math.round(P.tone_unevenness.percentile)}</Chip>}</dd><dt className="text-muted-foreground">Grupo de referencia</dt><dd>{String((k.percentiles as Record<string, unknown>)?.group ?? "–")} (n={String((k.percentiles as Record<string, unknown>)?.n ?? 0)})</dd><dt className="text-muted-foreground">Píxeles de piel</dt><dd className="tabular">{k.skin_pixels}</dd></dl><Cap>{k.note}</Cap></Card>
            <div><Photo src={out(k.maps.mask)} ratio="16/9" /><Cap>Máscara de piel derivada de la malla (sin ojos, cejas, labios ni fosas).</Cap></div>
          </Sci>
          <Regions R={R} state={st} />
        </>
      ) : st === "running" ? <div className="mt-6 grid grid-cols-2 gap-4 md:grid-cols-4">{[0, 1, 2, 3].map((i) => <Card key={i} className="p-3"><div className="sk aspect-square rounded-2xl" /><div className="sk mt-3 h-5 w-3/5" /></Card>)}</div>
      : <Empty className="mt-6">Análisis de piel no disponible.</Empty>}
    </Section>
  );
}

function Regions({ R, state }: { R: Report; state: string }) {
  const pg = R.parsing;
  return (
    <Sci className="mt-8">
      <h3 className="text-[20px] font-medium">Segmentación de la cara</h3>
      <Cap className="mt-0">Un segundo modelo separa piel, pelo, cejas, ojos, labios, orejas y cuello. De aquí sale la línea del pelo real.</Cap>
      <div className="mt-4 grid gap-4 md:grid-cols-2">
        <Photo src={out(R.assets?.parsing)} ratio="16/9" />
        <Card>
          {pg ? <dl className="grid grid-cols-[auto_1fr] gap-x-4 gap-y-1.5 text-[13.5px]"><dt className="text-muted-foreground">Línea del pelo</dt><dd>{pg.trichion_y != null ? `detectada · frente de ${pg.forehead_height_px} px` : "no detectada"}</dd><dt className="text-muted-foreground">Pelo visible</dt><dd>{pg.hair_visible ? "sí" : "no"}</dd><dt className="text-muted-foreground">Orejas visibles</dt><dd>{pg.ear_visible?.any ? "sí" : "no"}</dd><dt className="text-muted-foreground">Gafas</dt><dd>{pg.glasses ? "sí (afecta a ojos y cejas)" : "no"}</dd><dt className="text-muted-foreground">Cuello visible</dt><dd>{pg.neck_visible ? "sí" : "no"}</dd><dt className="text-muted-foreground">Gorro</dt><dd>{pg.hat ? "sí" : "no"}</dd></dl> : state === "running" ? <div className="sk h-24" /> : <p className="text-muted-foreground">Segmentación no disponible.</p>}
          {R.age && <><h4 className="mt-4 text-[15px] font-semibold">Edad visual: {R.age.visual_age} años</h4><Cap>{R.age.note}</Cap></>}
        </Card>
      </div>
    </Sci>
  );
}
