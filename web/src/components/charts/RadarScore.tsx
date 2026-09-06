/** Radar de marcos (0–100) en SVG puro: determinista, sin dependencias y se imprime igual en el PDF. */
export function RadarScore({ data, className, size = 320, color = "var(--coral)" }: { data: { k: string; v: number }[]; className?: string; size?: number; color?: string }) {
  const n = data.length; if (n < 3) return null;
  const cx = size / 2, cy = size / 2, r = size * 0.36;
  const pt = (i: number, v: number): [number, number] => { const a = -Math.PI / 2 + (i * 2 * Math.PI) / n; return [cx + Math.cos(a) * r * v / 100, cy + Math.sin(a) * r * v / 100]; };
  const poly = (v: number) => data.map((_, i) => pt(i, v).join(",")).join(" ");
  return (
    <svg viewBox={`0 0 ${size} ${size}`} className={className ?? "mx-auto block w-full max-w-[340px]"} role="img" aria-label="Radar de marcos">
      {[25, 50, 75, 100].map((g) => <polygon key={g} points={poly(g)} fill="none" stroke="var(--line-2)" strokeWidth={1} />)}
      {data.map((_, i) => { const [x, y] = pt(i, 100); return <line key={i} x1={cx} y1={cy} x2={x} y2={y} stroke="var(--line)" />; })}
      <polygon points={data.map((d, i) => pt(i, d.v).join(",")).join(" ")} fill={color} fillOpacity={0.18} stroke={color} strokeWidth={2} strokeLinejoin="round" />
      {data.map((d, i) => { const [x, y] = pt(i, d.v); const [lx, ly] = pt(i, 124); return (
        <g key={d.k}>
          <circle cx={x} cy={y} r={4} fill={color} stroke="var(--card)" strokeWidth={2} />
          <text x={lx} y={ly} fontSize={11} fontWeight={600} textAnchor="middle" dominantBaseline="middle" fill="var(--muted-ink)">{d.k}</text>
          <text x={lx} y={ly + 13} fontSize={10} textAnchor="middle" dominantBaseline="middle" fill="var(--ink)" className="tabular">{Math.round(d.v)}</text>
        </g>
      ); })}
    </svg>
  );
}
