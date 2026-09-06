import { cn } from "@/lib/utils";

/** Barra segmentada (tercios, quintos): cada tramo proporcional y con su porcentaje. */
export function Segments({ parts, colors, className, ideal }: { parts: { k: string; v: number; label?: string }[]; colors: string[]; className?: string; ideal?: number }) {
  return (
    <div className={className}>
      <div className="flex h-11 overflow-hidden rounded-2xl border border-line">
        {parts.map((p, i) => (
          <div key={p.k} className="flex items-center justify-center text-[12px] font-bold text-white" style={{ flex: p.v, background: colors[i % colors.length], boxShadow: "inset -2px 0 0 var(--paper)" }} title={p.label}>{Math.round(p.v * 100)}%</div>
        ))}
      </div>
      {ideal != null && <div className="mt-1.5 flex text-[10px] text-muted-foreground">{parts.map((p) => <span key={p.k} className="truncate text-center" style={{ flex: p.v }}>{p.label ?? p.k}</span>)}</div>}
    </div>
  );
}

export const cnx = cn;
