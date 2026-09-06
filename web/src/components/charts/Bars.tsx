"use client";
import { Bar, BarChart, Cell, LabelList, XAxis, YAxis } from "recharts";
import { ChartContainer, ChartTooltip, ChartTooltipContent, type ChartConfig } from "@/components/ui/chart";

const config = { v: { label: "Valor", color: "var(--coral)" } } satisfies ChartConfig;

/** Barras horizontales con etiqueta directa (ranking de estaciones, asimetría por punto, etc.). */
export function HBars({ data, unit = "", highlight, height = 200, color = "var(--lavender)", format }:
  { data: { k: string; v: number }[]; unit?: string; highlight?: string; height?: number; color?: string; format?: (v: number) => string }) {
  const fmt = format ?? ((v: number) => `${v}${unit}`);
  return (
    <ChartContainer config={config} className="w-full" style={{ height }} initialDimension={{ width: 560, height }}>
      <BarChart data={data} layout="vertical" margin={{ left: 0, right: 44, top: 4, bottom: 4 }} barCategoryGap={6}>
        <XAxis type="number" hide />
        <YAxis type="category" dataKey="k" width={150} tickLine={false} axisLine={false} tick={{ fill: "var(--ink-2)", fontSize: 12, fontWeight: 500 }} tickFormatter={(v: string) => (v.length > 24 ? `${v.slice(0, 23)}…` : v)} />
        <ChartTooltip cursor={{ fill: "var(--secondary)" }} content={<ChartTooltipContent formatter={(v) => fmt(Number(v))} />} />
        <Bar dataKey="v" radius={[4, 4, 4, 4]} barSize={14} isAnimationActive>
          {data.map((d) => <Cell key={d.k} fill={d.k === highlight ? "var(--coral)" : color} />)}
          <LabelList dataKey="v" position="right" formatter={(v: unknown) => fmt(Number(v))} style={{ fill: "var(--ink-2)", fontSize: 11, fontWeight: 600 }} />
        </Bar>
      </BarChart>
    </ChartContainer>
  );
}
