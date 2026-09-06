"use client";
import type { Report } from "@/lib/types";
import { out } from "@/lib/api";
import { Sci } from "@/lib/mode";
import { HBars } from "@/components/charts/Bars";
import { Ring } from "@/components/charts/Ring";
import { Section, SectionHead } from "@/components/site/Section";
import { Card, Cap, Photo } from "./bits";
import { Narrative } from "./Narrative";

export function Symmetry({ R, stepState, stepDetail }: { R: Report; stepState: (id: string) => string; stepDetail: (id: string) => string }) {
  const s = R.scores?.symmetry, sy = R.measures?.symmetry?.detail || {};
  const per = Object.entries(sy.per_landmark_pct || {}).sort((a, b) => b[1] - a[1]).slice(0, 6);
  return (
    <Section id="simetria">
      <SectionHead eyebrow="Simetría" title={<>Tu lado derecho <em className="italic text-coral">y tu lado izquierdo.</em></>} lede="Nadie es simétrico. Estas dos caras se construyen duplicando cada mitad; la diferencia entre ellas es tu asimetría." />
      <div className="mt-6 grid grid-cols-3 gap-3">
        <div><Photo src={out(R.assets?.mirror_left)} /><Cap>Mitad izquierda, duplicada</Cap></div>
        <div><Photo src={out(R.assets?.face)} /><Cap>Original</Cap></div>
        <div><Photo src={out(R.assets?.mirror_right)} /><Cap>Mitad derecha, duplicada</Cap></div>
      </div>
      <div className="mt-5 grid gap-5 md:grid-cols-2">
        <Card>
          <div className="flex items-center gap-5">
            <Ring value={s?.score} size={110} stroke={10} label="de 100" />
            <div>
              <div className="eyebrow">Índice de simetría</div>
              <p className="mt-1 text-[15px] leading-snug">{s ? <>Más simétrica que el <b>{Math.round(s.percentile)} %</b> de tu grupo.</> : "Calculando…"}</p>
              <Sci><Cap className="mt-1">Media del grupo {s?.group_mean}. Error medio {sy.mean_error_pct_face_height} % de la altura facial.</Cap></Sci>
            </div>
          </div>
          <Sci>{per.length > 0 && <div className="mt-4"><HBars data={per.map(([k, v]) => ({ k, v: +v.toFixed(2) }))} unit="%" height={190} format={(v) => `${v.toFixed(2)} %`} /><Cap>Puntos con más desviación (% de la altura facial).</Cap></div>}</Sci>
        </Card>
        <Narrative R={R} k="global" state={stepState("narrative")} detail={stepDetail("narrative")} />
      </div>
    </Section>
  );
}
