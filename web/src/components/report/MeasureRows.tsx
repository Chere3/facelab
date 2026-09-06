import type { Report } from "@/lib/types";
import { SUB, fmt, normText, band, plainLine } from "@/lib/plain";
import { PercentileBar } from "@/components/charts/PercentileBar";
import { Chip } from "@/components/site/Chip";

/** Tabla de medidas (modo ciencia): nombre, norma, valor, percentil. */
export function MeasureRows({ R, keys }: { R: Report; keys: string[] }) {
  const pm = R.norms?.per_measure || {};
  const rows: React.ReactNode[] = [];
  for (const k of keys) {
    const m = R.measures?.[k]; if (!m) continue;
    const c = R.catalog?.[k] || { name: k };
    const val = m.value;
    if (val && typeof val === "object") {
      for (const [kk, vv] of Object.entries(val)) {
        if (typeof vv !== "number") continue;
        const s = pm[`${k}.${kk}`];
        rows.push(<Row key={`${k}.${kk}`} name={c.name} tag={SUB[kk] || kk} norm={normText(c.norm)} value={fmt(vv)} unit={m.unit} p={s?.percentile} />);
      }
    } else rows.push(<Row key={k} name={c.name} norm={normText(c.norm) + (m.caveat ? ` · ${m.caveat}` : "")} value={fmt(val)} unit={m.unit} p={pm[k]?.percentile} />);
  }
  return <div className="divide-y divide-line">{rows}</div>;
}
function Row({ name, tag, norm, value, unit, p }: { name: string; tag?: string; norm: string; value: string; unit: string; p?: number }) {
  return (
    <div className="grid grid-cols-[minmax(0,1.3fr)_80px_minmax(0,1fr)] items-center gap-3 py-2.5">
      <div className="text-[13px] font-semibold">{name} {tag && <span className="ml-1 rounded-md bg-secondary px-1.5 py-0.5 text-[11px] font-medium text-muted-foreground">{tag}</span>}{norm && <small className="block text-[11px] leading-snug font-normal text-muted-foreground">{norm}</small>}</div>
      <div className="tabular text-right text-[13px] whitespace-nowrap">{value} <span className="font-mono text-[10px] text-muted-foreground">{unit}</span></div>
      <PercentileBar p={p} />
    </div>
  );
}

/** Lectura llana de las medidas de una zona: solo las que se alejan de la media (o las tres primeras). */
export function PlainMeasures({ R, keys, max = 4 }: { R: Report; keys: string[]; max?: number }) {
  const pm = R.norms?.per_measure || {};
  const items: { id: string; p: number; z: number }[] = [];
  for (const k of keys) {
    const m = R.measures?.[k]; if (!m) continue;
    if (m.value && typeof m.value === "object") {
      const subs = Object.keys(m.value).map((kk) => pm[`${k}.${kk}`]).filter(Boolean);
      if (subs.length) items.push({ id: k, p: subs.reduce((a, x) => a + x.percentile, 0) / subs.length, z: Math.max(...subs.map((x) => Math.abs(x.z ?? 0))) });
    } else if (pm[k]) items.push({ id: k, p: pm[k].percentile, z: Math.abs(pm[k].z ?? 0) });
  }
  items.sort((a, b) => b.z - a.z);
  const show = items.slice(0, max);
  if (!show.length) return null;
  return (
    <div className="flex flex-wrap gap-2">
      {show.map((it) => { const b = band(it.p); return <Chip key={it.id} tone={b === "mid" ? "ok" : b === "lo" ? "warn" : b === "hi" ? "lavender" : "neutral"}>{plainLine(it.id, it.p)}</Chip>; })}
    </div>
  );
}
