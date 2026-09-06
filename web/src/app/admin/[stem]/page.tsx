"use client";
import { use, useEffect, useState } from "react";
import Link from "next/link";
import { getReport, out, putReview } from "@/lib/api";
import type { Report } from "@/lib/types";
import { Nav } from "@/components/site/Nav";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Card } from "@/components/report/bits";

type Draft = { narrative: NonNullable<Report["narrative"]>; protocol: NonNullable<Report["protocol"]>; review: NonNullable<Report["review"]> };
const clone = <T,>(x: T): T => JSON.parse(JSON.stringify(x));

export default function ReviewPage({ params }: { params: Promise<{ stem: string }> }) {
  const { stem } = use(params);
  const [R, setR] = useState<Report | null>(null);
  const [d, setD] = useState<Draft | null>(null);
  const [msg, setMsg] = useState("");
  const load = () => getReport(stem).then((r) => { setR(r); if (r) setD({ narrative: clone(r.narrative || {}), protocol: clone(r.protocol || {}), review: clone(r.review || {}) }); });
  useEffect(() => { load(); }, [stem]); // eslint-disable-line react-hooks/exhaustive-deps
  const upd = (fn: (x: Draft) => void) => setD((x) => { if (!x) return x; const y = clone(x); fn(y); return y; });
  const save = async (approve: boolean) => {
    if (!d) return;
    const patch = clone(d);
    if (approve) { patch.review.approved = true; patch.review.at = new Date().toISOString().slice(0, 16).replace("T", " "); }
    try { await putReview(stem, patch); setMsg(approve ? "Aprobado y guardado" : "Guardado"); load(); } catch (e) { setMsg(`Error: ${(e as Error).message}`); }
  };
  const lines = (a?: string[]) => (a || []).join("\n"), split = (s: string) => s.split("\n").map((x) => x.trim()).filter(Boolean);
  const TA = (v: string | undefined, on: (s: string) => void, rows = 2) => <Textarea value={v || ""} rows={rows} onChange={(e) => on(e.target.value)} className="rounded-xl text-[13.5px]" />;

  if (!R || !d) return <><Nav /><div className="p-10 text-muted-foreground">Cargando…</div></>;
  return (
    <>
      <Nav />
      <div className="sticky top-[57px] z-20 glass border-b border-line"><div className="mx-auto flex max-w-[1100px] flex-wrap items-center gap-3 px-5 py-2.5 text-[13px] md:px-7"><Link href="/admin" className="text-coral">← Cola</Link><b>{stem}</b><span className="text-muted-foreground">{R.person}</span><span className="ml-auto" /><Input placeholder="Tu nombre" value={d.review.by || ""} onChange={(e) => upd((x) => { x.review.by = e.target.value; })} className="h-9 w-40 rounded-full" /><Button variant="outline" className="rounded-full" onClick={() => save(false)}>Guardar</Button><Button className="rounded-full" onClick={() => save(true)}>Guardar y aprobar</Button><span className="text-sage">{msg || (R.review?.approved ? `Revisado por ${R.review.by} · ${R.review.at}` : "")}</span></div></div>
      <main className="mx-auto grid max-w-[1100px] gap-6 px-5 py-6 md:grid-cols-[220px_1fr] md:px-7">
        <div><img src={out(R.assets?.face)} alt="" className="w-full rounded-2xl" /><p className="mt-2 text-[12px] text-muted-foreground">{R.norms?.group} · edad visual {R.age?.visual_age ?? "?"}</p><Link href={`/report/${stem}`} target="_blank" className="text-[13px] font-semibold text-coral">Ver informe →</Link></div>
        <div className="space-y-5">
          <Card><h2 className="mb-2 text-[16px] font-semibold">Notas del revisor</h2>{TA(d.review.notes, (s) => upd((x) => { x.review.notes = s; }))}</Card>
          <h2 className="text-[22px] font-medium">Narrativa</h2>
          {Object.entries(d.narrative).map(([sec, v]) => (
            <Card key={sec} className="space-y-3"><h3 className="text-[11px] font-bold tracking-widest text-coral uppercase">{sec.replace(/_/g, " ")}</h3>
              <Row label="Resumen">{TA(v.summary, (s) => upd((x) => { x.narrative[sec].summary = s; }), 3)}</Row>
              {(v.findings || []).map((f, i) => <Row key={i} label={f.measure}>{TA(f.statement, (s) => upd((x) => { x.narrative[sec].findings![i].statement = s; }))}</Row>)}
              <Row label="Puntos fuertes (uno por línea)">{TA(lines(v.strengths), (s) => upd((x) => { x.narrative[sec].strengths = split(s); }))}</Row>
              <Row label="A vigilar (uno por línea)">{TA(lines(v.watch), (s) => upd((x) => { x.narrative[sec].watch = split(s); }))}</Row>
            </Card>))}
          <h2 className="text-[22px] font-medium">Rutina</h2>
          {(d.protocol.phases || []).map((ph, i) => (
            <Card key={i} className="space-y-3"><h3 className="text-[11px] font-bold tracking-widest text-coral uppercase">{ph.name} · {ph.weeks}</h3>
              <Row label="Objetivo">{TA(ph.goal, (s) => upd((x) => { x.protocol.phases![i].goal = s; }))}</Row>
              {(ph.actions || []).map((a, j) => <Row key={j} label={a.name}>{TA(a.why, (s) => upd((x) => { x.protocol.phases![i].actions![j].why = s; }))}</Row>)}
            </Card>))}
          <Card className="space-y-3"><Row label="No hace falta tocar (uno por línea)">{TA(lines(d.protocol.not_recommended), (s) => upd((x) => { x.protocol.not_recommended = split(s); }), 3)}</Row><Row label="Carta">{TA(d.protocol.letter, (s) => upd((x) => { x.protocol.letter = s; }), 5)}</Row></Card>
        </div>
      </main>
    </>
  );
}
const Row = ({ label, children }: { label: string; children: React.ReactNode }) => <div className="grid gap-1.5 md:grid-cols-[200px_1fr] md:gap-3"><label className="pt-2 text-[12px] text-muted-foreground">{label}</label>{children}</div>;
