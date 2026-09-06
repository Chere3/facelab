"use client";
import { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { getReports, out } from "@/lib/api";
import type { ReportRow } from "@/lib/types";
import { Nav } from "@/components/site/Nav";
import { Footer } from "@/components/site/Footer";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

export default function PeoplePage() {
  const [l, setL] = useState<ReportRow[] | null>(null);
  const [sel, setSel] = useState<string[]>([]);
  const router = useRouter();
  useEffect(() => { getReports().then(setL).catch(() => setL([])); }, []);
  const groups: Record<string, ReportRow[]> = {};
  for (const r of l || []) (groups[r.person || "(sin nombre)"] ??= []).push(r);
  const toggle = (s: string) => setSel((x) => (x.includes(s) ? x.filter((y) => y !== s) : [...x, s].slice(-2)));
  return (
    <>
      <Nav />
      <main className="mx-auto max-w-[1240px] px-5 md:px-7">
        <div className="flex flex-wrap items-end justify-between gap-4 pt-10 pb-6">
          <div><div className="eyebrow mb-2">Personas</div><h1 className="text-[clamp(30px,3.6vw,46px)] font-medium">Personas <span className="gradient-text">y seguimiento.</span></h1><p className="mt-2 max-w-[60ch] text-muted-foreground">Cada persona con sus informes en el tiempo. Elige dos para comparar.</p></div>
          <Button className="rounded-full" disabled={sel.length !== 2} onClick={() => router.push(`/compare?a=${sel[0]}&b=${sel[1]}`)}>Comparar {sel.length}/2</Button>
        </div>
        {l == null ? <div className="sk h-40 rounded-3xl" /> : !l.length ? <p className="text-muted-foreground">Aún no hay informes.</p> : Object.entries(groups).map(([k, rs]) => {
          rs.sort((a, b) => (a.date || "").localeCompare(b.date || ""));
          return (
            <div key={k} className="card-soft mb-4 p-5">
              <h2 className="text-[22px] font-medium">{k} <span className="text-[13px] text-muted-foreground">· {rs.length} informe{rs.length > 1 ? "s" : ""}</span></h2>
              <div className="no-scrollbar mt-3 flex gap-3 overflow-x-auto">
                {rs.map((r) => (
                  <div key={r.stem} className={cn("w-[180px] shrink-0 rounded-2xl border p-2.5 transition", sel.includes(r.stem) ? "border-coral bg-coral-2" : "border-line")}>
                    <img src={out(r.face)} alt="" className="aspect-square w-full rounded-xl bg-secondary object-cover" />
                    <div className="mt-2 text-[12px] text-muted-foreground">{r.date}</div>
                    <div className="grid grid-cols-[1fr_auto] gap-x-2 text-[12px]">{Object.entries(r.scores || {}).map(([a, b]) => <span key={a} className="contents"><span className="text-muted-foreground">{a}</span><b className="tabular">{b ?? "–"}</b></span>)}</div>
                    <div className="mt-2 flex items-center gap-2"><Link href={`/report/${r.stem}`}><Button size="sm" variant="outline" className="rounded-full">Ver</Button></Link><label className="flex items-center gap-1 text-[12px]"><input type="checkbox" checked={sel.includes(r.stem)} onChange={() => toggle(r.stem)} />comparar</label></div>
                  </div>
                ))}
              </div>
            </div>
          );
        })}
      </main>
      <Footer />
    </>
  );
}
