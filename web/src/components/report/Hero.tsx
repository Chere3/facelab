"use client";
import { useState } from "react";
import type { Report, Status } from "@/lib/types";
import { out, regen } from "@/lib/api";
import { SEX, ANC, headlineChips, highlights } from "@/lib/plain";
import { Sci } from "@/lib/mode";
import { Ring } from "@/components/charts/Ring";
import { Chip } from "@/components/site/Chip";
import { Button } from "@/components/ui/button";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { ProsCons, WarnBox } from "./bits";

const AMB: Record<string, string> = { auto: "Ambición automática", mejora: "Ambición: mejorar", "glow-up": "Ambición: glow-up" };

/** Cabecera del dashboard: foto, titular, KPIs en anillos, avisos, pros/contras y acciones. */
export function Hero({ R, status, stem, onWake, stepState }: { R: Report; status: Status | null; stem: string; onWake: () => void; stepState: (id: string) => string }) {
  const s = R.scores || {}, pr = R.profile || {};
  const face = out(R.assets?.face);
  const first = R.person?.split(" ")[0];
  const chips = headlineChips(R);
  const { strengths, watch } = highlights(R);
  const [amb, setAmb] = useState(pr.ambition || "auto");
  const [busy, setBusy] = useState<string | null>(null);
  const go = async (steps: string[]) => { setBusy(steps.join()); try { await regen(stem, steps, amb !== "auto" ? { ambition: amb } : {}); onWake(); } finally { setBusy(null); } };
  const pdf = async () => {
    setBusy("pdf");
    try { const r = await fetch(`/api/pdf/${stem}`); if (!r.ok) { alert((await r.json().catch(() => ({}))).error || "No se pudo generar el PDF"); return; } const a = document.createElement("a"); a.href = URL.createObjectURL(await r.blob()); a.download = `informe-${stem}.pdf`; a.click(); } finally { setBusy(null); }
  };
  const G = s.global?.composite;
  const running = status && !status.done;

  return (
    <div className="flex flex-col gap-5">
      <div className="grid gap-5 md:grid-cols-[minmax(0,4fr)_minmax(0,8fr)]">
        {/* foto con chips */}
        <div className={`panel relative aspect-square overflow-hidden p-0 ${face ? "" : "sk"}`}>
          {face && <img src={face} alt="Tu cara alineada" className="size-full object-cover" />}
          <div className="absolute inset-x-0 bottom-0 bg-gradient-to-t from-black/80 to-transparent p-4 pt-16">
            <div className="text-[11px] font-bold tracking-[0.16em] text-white/70 uppercase">Tu informe · {R.date || ""}</div>
            <div className="mt-1 flex flex-wrap gap-1.5">{chips.map((c) => <Chip key={c.label} tone={c.tone === "ok" ? "ok" : "neutral"} dot={c.hex} size="sm" className="border-white/15 bg-black/40 text-white backdrop-blur">{c.label}</Chip>)}</div>
          </div>
        </div>

        <div className="flex flex-col gap-5">
          <div className="panel p-6 md:p-7">
            <h1 className="text-[clamp(30px,3.6vw,46px)] leading-[1.02]">
              {first ? `${first}, esto` : "Esto"} es lo que <span className="gradient-text">tu cara</span> ya dice de ti.
            </h1>
            <p className="mt-3 max-w-[60ch] text-[14.5px] text-muted-foreground">
              Medimos {Object.keys(R.norms?.per_measure || {}).length} proporciones y las comparamos con {R.norms?.n ?? 0} personas parecidas a ti. Sin notas de belleza: qué juega a tu favor, tus colores, tu rutina y cómo te verías.
            </p>
            <Sci className="mt-3 flex flex-wrap gap-1.5">
              <Chip size="sm">{SEX[pr.sex ?? ""] || "sin sexo declarado"}</Chip><Chip size="sm">{ANC[pr.ancestry ?? ""] || "sin ascendencia declarada"}</Chip>{pr.age ? <Chip size="sm">{pr.age} años</Chip> : null}
              <Chip size="sm" tone={R.warnings?.length ? "warn" : "ok"}>{R.warnings?.length ? "foto con avisos" : "foto válida"}</Chip>
              {R.review?.approved ? <Chip size="sm" tone="ok">revisado por {R.review.by || "equipo"}</Chip> : <Chip size="sm" tone="warn">pendiente de revisión humana</Chip>}
            </Sci>
            <div className="no-print mt-4 flex flex-wrap items-center gap-2">
              <Button onClick={pdf} disabled={busy === "pdf"} className="btn-glow rounded-full border-0">{busy === "pdf" ? "Generando PDF…" : "Descargar PDF"}</Button>
              <Button variant="outline" className="rounded-full" disabled={!!running} onClick={() => go(["narrative", "protocol", "visualize"])}>Regenerar todo</Button>
              <Button variant="outline" className="rounded-full" disabled={!!running} onClick={() => go(["narrative"])}>Solo narrativa</Button>
              <Button variant="outline" className="rounded-full" disabled={!!running} onClick={() => go(["protocol", "visualize"])}>Rutina + imagen</Button>
              <Select value={amb} onValueChange={(v) => setAmb(String(v))} items={AMB}>
                <SelectTrigger className="w-[190px] rounded-full"><SelectValue /></SelectTrigger>
                <SelectContent>{Object.entries(AMB).map(([v, l]) => <SelectItem key={v} value={v}>{l}</SelectItem>)}</SelectContent>
              </Select>
            </div>
          </div>
          <div className="grid grid-cols-3 gap-3 sm:grid-cols-5">
            <Tile v={s.symmetry?.score} label="Simetría" sub={s.symmetry ? `percentil ${Math.round(s.symmetry.percentile)}` : undefined} />
            <Tile v={s.averageness?.score} label="Armonía" sub="cerca de la media" color="var(--violet)" />
            <Tile v={s.proportionality?.score} label="Proporción" sub="17 ratios" color="var(--mint)" />
            {G && <Tile v={G.score} label="Global" sub="0–100" color="var(--peach)" />}
            {R.age ? <Tile v={R.age.visual_age} max={90} label="Edad visual" sub="±6–8 años" color="var(--sky)" /> : stepState("visual") === "running" ? <div className="sk rounded-3xl" /> : null}
          </div>
        </div>
      </div>
      {R.warnings?.map((w) => <WarnBox key={w}>{w}</WarnBox>)}
      <ProsCons pros={strengths} cons={watch} />
    </div>
  );
}

function Tile({ v, max = 100, label, sub, color = "var(--coral)" }: { v?: number | null; max?: number; label: string; sub?: string; color?: string }) {
  return (
    <div className="panel flex flex-col items-center px-2 py-3.5 text-center">
      <Ring value={v} max={max} size={64} stroke={6} color={color} track="var(--surface-3)" />
      <b className="mt-2 block font-display text-[13px] leading-tight">{label}</b>{sub && <small className="mt-0.5 block text-[10.5px] leading-tight text-muted-foreground">{sub}</small>}
    </div>
  );
}
