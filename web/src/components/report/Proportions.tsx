"use client";
import type { Report } from "@/lib/types";
import { out } from "@/lib/api";
import { Sci, Simple } from "@/lib/mode";
import { Segments } from "@/components/charts/Segments";
import { Section, SectionHead } from "@/components/site/Section";
import { Card, Cap, Photo } from "./bits";
import { MeasureRows, PlainMeasures } from "./MeasureRows";
import { Narrative } from "./Narrative";

const THIRD_COLORS = ["#c9b8ff", "var(--lavender)", "#6b48e0"];
const FIFTH_COLORS = ["#ffd3bb", "var(--peach)", "var(--coral)", "var(--peach)", "#ffd3bb"];
const KEYS = ["facial_thirds", "facial_fifths", "facial_index", "fwhr", "midface_ratio"];

export function Proportions({ R, stepState, stepDetail }: { R: Report; stepState: (id: string) => string; stepDetail: (id: string) => string }) {
  const th = R.measures?.facial_thirds, f = R.measures?.facial_fifths?.value as Record<string, number> | undefined;
  const t = th?.value as Record<string, number> | undefined, tt = th?.true;
  const thirds = (o: Record<string, number>) => [{ k: "upper", v: o.upper ?? o.upper_proxy, label: "frente" }, { k: "middle", v: o.middle, label: "nariz" }, { k: "lower", v: o.lower, label: "boca y mentón" }];
  return (
    <Section id="proporciones">
      <SectionHead eyebrow="Proporciones" title={<>Tercios <em className="italic text-coral">y quintos.</em></>} lede="El canon divide la cara en tres alturas y cinco anchuras iguales. Casi nadie lo cumple; lo útil es ver dónde te alejas." />
      <div className="mt-6 grid gap-6 md:grid-cols-2">
        <div><Photo src={out(R.assets?.guides)} ratio="4/5" alt="Guías" /><Cap>Horizontales: frente, glabela, subnasal, mentón. Verticales: cantos de los ojos.</Cap></div>
        <div className="space-y-4">
          <Card>
            <h3 className="text-[15px] font-semibold">Tercios verticales</h3>
            {tt ? <><Segments parts={thirds(tt)} colors={THIRD_COLORS} ideal={0.33} className="mt-2" /><Cap>Medidos hasta la línea del pelo real.</Cap></> : stepState("visual") === "running" ? <div className="sk my-2 h-11" /> : null}
            {t && <Sci><Segments parts={thirds(t)} colors={THIRD_COLORS} className="mt-3" /><Cap>Con el punto más alto de la malla como techo (orientativo arriba).</Cap></Sci>}
            {f && <><h3 className="mt-5 text-[15px] font-semibold">Quintos horizontales</h3>
              <Segments parts={[{ k: "outer_R", v: f.outer_R, label: "sien" }, { k: "eye_R", v: f.eye_R, label: "ojo" }, { k: "intercanthal", v: f.intercanthal, label: "entre ojos" }, { k: "eye_L", v: f.eye_L, label: "ojo" }, { k: "outer_L", v: f.outer_L, label: "sien" }]} colors={FIFTH_COLORS} ideal={0.2} className="mt-2" />
              <Cap>Ideal del canon: 20 % cada uno.</Cap></>}
          </Card>
          <Simple><PlainMeasures R={R} keys={KEYS} /></Simple>
          <Sci><Card><MeasureRows R={R} keys={KEYS} /></Card></Sci>
          <Narrative R={R} k="proporciones" state={stepState("narrative")} detail={stepDetail("narrative")} />
        </div>
      </div>
    </Section>
  );
}
