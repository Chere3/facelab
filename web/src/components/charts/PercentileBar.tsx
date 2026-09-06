import { band } from "@/lib/plain";
import { cn } from "@/lib/utils";

/** Barra de percentil con la franja típica (25–75) marcada y el marcador de la persona. */
export function PercentileBar({ p, className, labels = true }: { p: number | null | undefined; className?: string; labels?: boolean }) {
  if (p == null) return <div className={cn("text-[11px] text-muted-foreground", className)}>sin comparación</div>;
  const b = band(p);
  const color = b === "lo" ? "var(--apricot)" : b === "hi" ? "var(--lavender)" : "var(--coral)";
  return (
    <div className={className}>
      <div className="relative h-2 rounded-full" style={{ background: "linear-gradient(90deg, var(--apricot-2) 0 25%, var(--secondary) 25% 75%, var(--lavender-2) 75% 100%)" }}>
        <i className="absolute -top-1 size-4 -translate-x-1/2 rounded-full border-[3px] border-paper shadow-[0_0_0_1px_var(--line-2)]" style={{ left: `${p}%`, background: color }} />
      </div>
      {labels && <div className="mt-1 flex justify-between text-[10px] text-muted-foreground"><span>p0</span><b className="text-ink">p{Math.round(p)}</b><span>p100</span></div>}
    </div>
  );
}

export function PctChip({ p, className }: { p: number | null | undefined; className?: string }) {
  const b = band(p);
  const cls = b === "lo" ? "bg-apricot-2 text-apricot" : b === "hi" ? "bg-lavender-2 text-lavender" : b == null ? "bg-secondary text-muted-foreground" : "bg-coral-2 text-coral";
  return <span className={cn("rounded-md px-2 py-0.5 text-[11px] font-bold whitespace-nowrap", cls, className)}>{p == null ? "s/p" : `p${Math.round(p)}`}</span>;
}
