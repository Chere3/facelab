import { cn } from "@/lib/utils";

/** Anillo de progreso con cifra grande en el centro. Se dibuja completo en el servidor (PDF) y se anima por CSS en el navegador. */
export function Ring({ value, max = 100, size = 96, stroke = 9, color = "var(--coral)", track = "var(--line)", label, sub, className, children }:
  { value: number | null | undefined; max?: number; size?: number; stroke?: number; color?: string; track?: string; label?: React.ReactNode; sub?: React.ReactNode; className?: string; children?: React.ReactNode }) {
  const p = Math.max(0, Math.min(1, (value ?? 0) / max));
  const r = (size - stroke) / 2, c = 2 * Math.PI * r;
  return (
    <div className={cn("relative inline-flex items-center justify-center", className)} style={{ width: size, height: size }}>
      <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`} className="-rotate-90">
        <circle cx={size / 2} cy={size / 2} r={r} fill="none" stroke={track} strokeWidth={stroke} />
        <circle cx={size / 2} cy={size / 2} r={r} fill="none" stroke={color} strokeWidth={stroke} strokeLinecap="round" strokeDasharray={c} strokeDashoffset={c * (1 - p)} className="ring-anim" style={{ ["--c" as string]: c }} />
      </svg>
      <div className="absolute inset-0 flex flex-col items-center justify-center text-center leading-none">
        {children ?? (<><b className="tabular font-display" style={{ fontSize: size * 0.28 }}>{value == null ? "–" : Math.round(value)}</b>{label && <span className="mt-1 text-[10px] font-medium text-muted-foreground">{label}</span>}</>)}
      </div>
      {sub}
    </div>
  );
}
