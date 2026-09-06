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
import { Photo, ProsCons, WarnBox } from "./bits";

const AMB: Record<string, string> = { auto: "Ambición automática", mejora: "Ambición: mejorar", "glow-up": "Ambición: glow-up" };

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
    <div className="grid items-center gap-8 pt-6 md:grid-cols-[minmax(0,5fr)_minmax(0,7fr)] md:gap-12 md:pt-10">
      <div className="relative">
        <Photo src={face} alt="Tu cara alineada" className="rounded-[40px] shadow-lift" />
        {chips.slice(0, 3).map((c, i) => (
          <span key={c.label} className="absolute animate-in fade-in slide-in-from-bottom-2 duration-700" style={{ [i === 1 ? "right" : "left"]: i === 0 ? "-4%" : i === 1 ? "-2%" : "8%", top: i === 0 ? "12%" : i === 1 ? "52%" : "auto", bottom: i === 2 ? "8%" : "auto", animationDelay: `${300 + i * 200}ms` }}>
            <Chip tone={c.tone === "ok" ? "ok" : "neutral"} dot={c.hex} size="lg" className="shadow-soft">{c.label}</Chip>
          </span>
        ))}
      </div>
      <div>
        <div className="eyebrow mb-3">Tu informe · {R.date || ""}</div>
        <h1 className="text-[clamp(38px,5.2vw,66px)] leading-[0.98] font-medium">
          {first ? `${first}, esto` : "Esto"} es lo que <em className="italic text-coral">tu cara</em> ya dice de ti.
        </h1>
        <p className="mt-4 max-w-[56ch] text-[16px] text-muted-foreground">
          Medimos {Object.keys(R.norms?.per_measure || {}).length} proporciones y las comparamos con {R.norms?.n ?? 0} personas parecidas a ti. Sin notas de belleza: qué juega a tu favor, tus colores, tu rutina y cómo te verías.
        </p>
        <Sci className="mt-2 flex flex-wrap gap-1.5 text-[12px]">
          <Chip size="sm">{SEX[pr.sex ?? ""] || "sin sexo declarado"}</Chip><Chip size="sm">{ANC[pr.ancestry ?? ""] || "sin ascendencia declarada"}</Chip>{pr.age ? <Chip size="sm">{pr.age} años</Chip> : null}
          <Chip size="sm" tone={R.warnings?.length ? "warn" : "ok"}>{R.warnings?.length ? "foto con avisos" : "foto válida"}</Chip>
          {R.review?.approved ? <Chip size="sm" tone="ok">revisado por {R.review.by || "equipo"}</Chip> : <Chip size="sm" tone="warn">pendiente de revisión humana</Chip>}
        </Sci>

        <div className="mt-6 flex flex-wrap gap-3">
          <Tile v={s.symmetry?.score} label="Simetría" sub={s.symmetry ? `p${Math.round(s.symmetry.percentile)}` : undefined} />
          <Tile v={s.averageness?.score} label="Armonía" sub="cerca de la media" color="var(--lavender)" />
          <Tile v={s.proportionality?.score} label="Proporción" sub="17 ratios" color="var(--sage)" />
          {G && <Tile v={G.score} label="Global" sub="0–100" color="var(--ink)" />}
          {R.age ? <Tile v={R.age.visual_age} max={90} label="Edad visual" sub="±6–8 años" color="var(--peach)" /> : stepState("visual") === "running" ? <div className="sk size-[104px] rounded-3xl" /> : null}
        </div>
        {R.warnings?.map((w) => <WarnBox key={w} className="mt-4">{w}</WarnBox>)}
        <ProsCons pros={strengths} cons={watch} className="mt-5" />

        <div className="no-print mt-5 flex flex-wrap items-center gap-2">
          <Button onClick={pdf} disabled={busy === "pdf"} className="rounded-full">{busy === "pdf" ? "Generando PDF…" : "Descargar PDF"}</Button>
          <Button variant="outline" className="rounded-full" disabled={!!running} onClick={() => go(["narrative", "protocol", "visualize"])}>Regenerar todo</Button>
          <Button variant="outline" className="rounded-full" disabled={!!running} onClick={() => go(["narrative"])}>Solo narrativa</Button>
          <Button variant="outline" className="rounded-full" disabled={!!running} onClick={() => go(["protocol", "visualize"])}>Rutina + imagen</Button>
          <Select value={amb} onValueChange={(v) => setAmb(String(v))} items={AMB}>
            <SelectTrigger className="w-[190px] rounded-full"><SelectValue /></SelectTrigger>
            <SelectContent>{Object.entries(AMB).map(([v, l]) => <SelectItem key={v} value={v}>{l}</SelectItem>)}</SelectContent>
          </Select>
        </div>
      </div>
    </div>
  );
}

function Tile({ v, max = 100, label, sub, color = "var(--coral)" }: { v?: number | null; max?: number; label: string; sub?: string; color?: string }) {
  return (
    <div className="card-soft flex w-[104px] flex-col items-center px-2 pt-3 pb-2.5">
      <Ring value={v} max={max} size={64} stroke={7} color={color} />
      <b className="mt-1 text-[12px]">{label}</b>
      {sub && <small className="text-[10px] text-muted-foreground">{sub}</small>}
    </div>
  );
}
