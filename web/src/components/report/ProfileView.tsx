"use client";
import type { Report } from "@/lib/types";
import { out } from "@/lib/api";
import { PROFILE_NAMES, fmt } from "@/lib/plain";
import { Sci } from "@/lib/mode";
import { Section, SectionHead } from "@/components/site/Section";
import { Chip } from "@/components/site/Chip";
import { Card, Cap, Empty, ErrBox, Photo, Skeleton, WarnBox } from "./bits";
import { Narrative } from "./Narrative";

const ORIENT = new Set(["gonial_soft", "submental_cervical", "mentolabial"]);

export function ProfileView({ R, stepState, stepDetail }: { R: Report; stepState: (id: string) => string; stepDetail: (id: string) => string }) {
  const pv = R.profile_view, st = stepState("profile");
  let inner: React.ReactNode;
  if (pv?.measures) {
    inner = (
      <div className="mt-6 grid gap-6 md:grid-cols-[minmax(0,5fr)_minmax(0,7fr)]">
        <div><Photo src={out(pv.image)} ratio="4/5" fit="contain" /><Cap>Silueta por segmentación con los puntos cefalométricos. Línea ámbar: línea E de Ricketts.</Cap></div>
        <div className="space-y-4">
          <Card>
            <div className="divide-y divide-line">
              {Object.entries(pv.measures).map(([k, v]) => (
                <div key={k} className="grid grid-cols-[minmax(0,1.4fr)_90px_minmax(0,1fr)] items-center gap-3 py-2.5 text-[13px]">
                  <div className="font-semibold">{PROFILE_NAMES[k] || k} {ORIENT.has(k) && <Chip size="sm" className="ml-1">orientativo</Chip>}<Sci><small className="block text-[11px] font-normal text-muted-foreground">{v.source}</small></Sci></div>
                  <div className="tabular text-right">{fmt(v.value)}<span className="font-mono text-[10px] text-muted-foreground"> {k.includes("ratio") || k.includes("eline") ? "ratio" : "°"}</span></div>
                  <div className="text-[12px] text-muted-foreground">norma {v.range || "–"}</div>
                </div>
              ))}
            </div>
          </Card>
          {!!pv.warnings?.length && <WarnBox>{pv.warnings.join(" · ")}</WarnBox>}
          <Narrative R={R} k="perfil" state={stepState("narrative")} detail={stepDetail("narrative")} />
        </div>
      </div>
    );
  } else if (st === "running") inner = <div className="mt-6 grid gap-6 md:grid-cols-2"><Photo ratio="4/5" /><Skeleton label="Midiendo el perfil…" lines={6} /></div>;
  else if (st === "error") inner = <ErrBox className="mt-5">El perfil falló: {stepDetail("profile")}</ErrBox>;
  else inner = <Empty className="mt-5">Sin foto de perfil. Súbela junto a la frontal para medir los ángulos reales de nariz, labios y mentón.</Empty>;
  return (
    <Section id="perfil">
      <SectionHead eyebrow="Perfil" title={<>Tu perfil, <em className="italic text-coral">medido de verdad.</em></>} lede="Con una foto lateral los ángulos dejan de ser estimados: se leen sobre la silueta real de tu cara." />
      {inner}
    </Section>
  );
}
