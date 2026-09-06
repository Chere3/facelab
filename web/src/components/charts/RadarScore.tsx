"use client";
import { PolarAngleAxis, PolarGrid, PolarRadiusAxis, Radar, RadarChart } from "recharts";
import { ChartContainer, ChartTooltip, ChartTooltipContent, type ChartConfig } from "@/components/ui/chart";

const config = { v: { label: "Puntuación", color: "var(--coral)" } } satisfies ChartConfig;

export function RadarScore({ data, className }: { data: { k: string; v: number }[]; className?: string }) {
  return (
    <ChartContainer config={config} className={className ?? "mx-auto aspect-square w-full max-w-[340px]"} initialDimension={{ width: 320, height: 320 }}>
      <RadarChart data={data} outerRadius="72%">
        <PolarGrid stroke="var(--line-2)" gridType="polygon" radialLines={false} />
        <PolarRadiusAxis domain={[0, 100]} tick={false} axisLine={false} />
        <PolarAngleAxis dataKey="k" tick={{ fill: "var(--muted-foreground)", fontSize: 11, fontWeight: 600 }} />
        <ChartTooltip cursor={false} content={<ChartTooltipContent hideLabel={false} />} />
        <Radar dataKey="v" fill="var(--coral)" fillOpacity={0.18} stroke="var(--coral)" strokeWidth={2} dot={{ r: 3.5, fill: "var(--coral)", strokeWidth: 0 }} isAnimationActive />
      </RadarChart>
    </ChartContainer>
  );
}
