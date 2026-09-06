"use client";
import { Suspense, useEffect, useState } from "react";
import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { getReport, out } from "@/lib/api";
import type { Report } from "@/lib/types";
import { plainName } from "@/lib/plain";
import { Nav } from "@/components/site/Nav";
import { Footer } from "@/components/site/Footer";
import { HBars } from "@/components/charts/Bars";
import { Card } from "@/components/report/bits";
import { cn } from "@/lib/utils";

export default function ComparePage() { return <Suspense><Compare /></Suspense>; }

function Compare() {
  const q = useSearchParams();
  const [A, setA] = useState<Report | null>(null), [B, setB] = useState<Report | null>(null);
  useEffect(() => { const a = q.get("a"), b = q.get("b"); if (a && b) Promise.all([getReport(a), getReport(b)]).then(([x, y]) => { setA(x); setB(y); }); }, [q]);
  const S = ["symmetry", "averageness", "proportionality"] as const;
  const SK = ["redness_pct", "spots_pct", "texture_index", "shine_pct", "tone_unevenness"] as const;
  let rows: [string, number, number][] = [];
  if (A && B) { const pa = A.norms?.per_measure || {}, pb = B.norms?.per_measure || {}; rows = Object.keys(pa).filter((k) => pb[k]).map((k) => [k, pa[k].percentile, pb[k].percentile]); rows.sort((x, y) => Math.abs(y[2] - y[1]) - Math.abs(x[2] - x[1])); }
  const D = ({ v, invert }: { v: number; invert?: boolean }) => <b className={cn("tabular", (invert ? v < 0 : v > 0) ? "text-sage" : v === 0 ? "" : "text-apricot")}>{v > 0 ? "+" : ""}{v.toFixed(1)}</b>;
  return (
    <>
      <Nav />
      <main className="mx-auto max-w-[1240px] px-5 md:px-7">
        <div className="pt-10 pb-6"><div className="eyebrow mb-2"><Link href="/people">← Personas</Link></div><h1 className="text-[clamp(30px,3.6vw,46px)] font-medium">Comparación <span className="gradient-text">en el tiempo.</span></h1>{A && B && <p className="mt-2 text-muted-foreground">{A.person} · {A.date} → {B.date}</p>}</div>
        {!A || !B ? <div className="sk h-60 rounded-3xl" /> : (
          <div className="space-y-5">
            <div className="grid max-w-[560px] grid-cols-2 gap-4">{[A, B].map((R, i) => <div key={i}><img src={out(R.assets?.face)} alt="" className="w-full rounded-3xl" /><div className="mt-1 text-[12px] text-muted-foreground">{R.date}</div></div>)}</div>
            <div className="grid gap-5 md:grid-cols-2">
              <Card><h2 className="text-[18px] font-semibold">Scores</h2><table className="mt-2 w-full text-[13.5px]"><thead><tr className="text-left text-[11px] text-muted-foreground"><th className="py-1 font-medium">Score</th><th className="font-medium">Antes</th><th className="font-medium">Después</th><th className="font-medium">Δ</th></tr></thead><tbody>
                {S.map((k) => { const a = A.scores?.[k]?.score ?? 0, b = B.scores?.[k]?.score ?? 0; return <tr key={k} className="border-t border-line"><td className="py-1.5">{k}</td><td className="tabular">{a}</td><td className="tabular">{b}</td><td><D v={b - a} /></td></tr>; })}
                <tr className="border-t border-line"><td className="py-1.5">edad visual</td><td>{A.age?.visual_age ?? "–"}</td><td>{B.age?.visual_age ?? "–"}</td><td /></tr></tbody></table></Card>
              <Card><h2 className="text-[18px] font-semibold">Piel <span className="text-[12px] font-normal text-muted-foreground">(menos es mejor)</span></h2><table className="mt-2 w-full text-[13.5px]"><thead><tr className="text-left text-[11px] text-muted-foreground"><th className="py-1 font-medium">Métrica</th><th className="font-medium">Antes</th><th className="font-medium">Después</th><th className="font-medium">Δ</th></tr></thead><tbody>
                {SK.map((k) => { const a = A.skin?.[k], b = B.skin?.[k]; if (a == null || b == null) return null; return <tr key={k} className="border-t border-line"><td className="py-1.5">{k}</td><td className="tabular">{a}</td><td className="tabular">{b}</td><td><D v={b - a} invert /></td></tr>; })}</tbody></table></Card>
            </div>
            <Card><h2 className="text-[18px] font-semibold">Percentiles por medida <span className="text-[12px] font-normal text-muted-foreground">(mayor cambio primero)</span></h2>
              <HBars data={rows.slice(0, 12).map(([k, a, b]) => ({ k: plainName(k, A.catalog), v: Math.round(b - a) }))} height={380} format={(v) => `${v > 0 ? "+" : ""}${v} p`} />
              <p className="mt-2 text-[12px] text-muted-foreground">Cambios menores de ±10 puntos entran en el ruido de medida entre fotos (luz, pose y expresión).</p></Card>
          </div>
        )}
      </main>
      <Footer />
    </>
  );
}
