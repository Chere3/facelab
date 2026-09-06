"use client";
import { useEffect, useState } from "react";
import Link from "next/link";
import { getReports, out } from "@/lib/api";
import type { ReportRow } from "@/lib/types";
import { Nav } from "@/components/site/Nav";
import { Footer } from "@/components/site/Footer";
import { Chip } from "@/components/site/Chip";
import { Button } from "@/components/ui/button";

export default function AdminPage() {
  const [l, setL] = useState<ReportRow[] | null>(null);
  useEffect(() => { getReports().then(setL).catch(() => setL([])); }, []);
  return (
    <>
      <Nav />
      <main className="mx-auto max-w-[1100px] px-5 md:px-7">
        <div className="pt-10 pb-6"><div className="eyebrow mb-2">Revisión</div><h1 className="text-[clamp(30px,3.6vw,46px)] font-medium">Cola <span className="gradient-text">de revisión.</span></h1><p className="mt-2 text-muted-foreground">Cada informe se edita y aprueba antes de marcarlo como revisado.</p></div>
        {l == null ? <div className="sk h-40 rounded-3xl" /> : (
          <div className="card-soft overflow-hidden p-0">
            <table className="w-full text-[14px]"><thead><tr className="text-left text-[11px] tracking-wider text-muted-foreground uppercase"><th className="p-3"></th><th className="p-3 font-medium">Informe</th><th className="p-3 font-medium">Persona</th><th className="p-3 font-medium">Perfil</th><th className="p-3 font-medium">Estado</th><th></th></tr></thead>
              <tbody>{l.map((r) => (
                <tr key={r.stem} className="border-t border-line">
                  <td className="p-3">{r.face && <img src={out(r.face)} alt="" className="size-11 rounded-xl object-cover" />}</td>
                  <td className="p-3"><Link href={`/report/${r.stem}`} className="font-semibold hover:text-coral">{r.stem}</Link><div className="text-[12px] text-muted-foreground">{r.date}</div></td>
                  <td className="p-3">{r.person || "—"}</td>
                  <td className="p-3 text-muted-foreground">{r.profile?.sex || "?"} · {r.profile?.ancestry || "?"}</td>
                  <td className="p-3">{r.review?.approved ? <Chip tone="ok" size="sm">revisado</Chip> : r.has_narrative ? <Chip tone="warn" size="sm">pendiente</Chip> : <span className="text-[12px] text-muted-foreground">generando</span>}</td>
                  <td className="p-3 text-right"><Link href={`/admin/${r.stem}`}><Button size="sm" variant="outline" className="rounded-full">Revisar</Button></Link></td>
                </tr>))}</tbody></table>
          </div>
        )}
      </main>
      <Footer />
    </>
  );
}
