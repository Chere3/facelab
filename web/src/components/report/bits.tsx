"use client";
import { cn } from "@/lib/utils";
import { simplify } from "@/lib/plain";
import { useMode } from "@/lib/mode";

export function Skeleton({ label, lines = 4, className }: { label?: string; lines?: number; className?: string }) {
  return (
    <div className={cn("card-soft p-5", className)}>
      {label && <div className="mb-3 flex items-center gap-2 text-[12px] text-muted-foreground"><i className="size-2 animate-pulse rounded-full bg-coral" />{label}</div>}
      {Array.from({ length: lines }).map((_, i) => <div key={i} className="sk my-2.5 h-3" style={{ width: i % 3 === 1 ? "88%" : i % 3 === 2 ? "70%" : "100%" }} />)}
    </div>
  );
}
export const Photo = ({ src, alt = "", className, ratio = "1/1", fit = "cover" }: { src?: string; alt?: string; className?: string; ratio?: string; fit?: "cover" | "contain" }) => (
  <div className={cn("overflow-hidden rounded-3xl bg-secondary", !src && "sk", className)} style={{ aspectRatio: ratio }}>
    {src && <img src={src} alt={alt} className={cn("size-full", fit === "cover" ? "object-cover" : "object-contain bg-white")} />}
  </div>
);
export const Cap = ({ children, className }: { children: React.ReactNode; className?: string }) => <div className={cn("mt-2 text-[12px] leading-snug text-muted-foreground", className)}>{children}</div>;
export const WarnBox = ({ children, className }: { children: React.ReactNode; className?: string }) => <div className={cn("rounded-2xl border-l-4 border-apricot bg-apricot-2 px-4 py-3 text-[14px]", className)}>{children}</div>;
export const ErrBox = ({ children, className }: { children: React.ReactNode; className?: string }) => <div className={cn("rounded-2xl border-l-4 border-destructive bg-[#fbe3e0] px-4 py-3 text-[14px]", className)}>{children}</div>;
export const Empty = ({ children, className }: { children: React.ReactNode; className?: string }) => <div className={cn("rounded-3xl border border-dashed border-line-2 p-7 text-center text-[14px] text-muted-foreground", className)}>{children}</div>;
export const Card = ({ children, className, soft }: { children: React.ReactNode; className?: string; soft?: boolean }) => <div className={cn("card-soft p-5", soft && "bg-gradient-to-b from-lavender-2/60 to-paper", className)}>{children}</div>;

/** Dos cajas: lo que juega a favor y dónde hay margen. */
export function ProsCons({ pros, cons, titles = ["Lo que juega a tu favor", "Dónde hay margen"], className }: { pros: string[]; cons: string[]; titles?: [string, string]; className?: string }) {
  const { mode } = useMode();
  if (!pros.length && !cons.length) return null;
  if (mode === "simple") { pros = pros.slice(0, 3).map(simplify); cons = cons.slice(0, 3).map(simplify); }
  return (
    <div className={cn("grid gap-3 sm:grid-cols-2", className)}>
      {pros.length > 0 && <div className="rounded-3xl bg-sage-2 p-4"><h4 className="mb-2 text-[11px] font-bold tracking-[0.12em] text-sage uppercase">{titles[0]}</h4><ul className="space-y-1.5 text-[13.5px] leading-snug">{pros.map((x, i) => <li key={i} className="flex gap-2"><span className="mt-2 size-1.5 shrink-0 rounded-full bg-sage" />{x}</li>)}</ul></div>}
      {cons.length > 0 && <div className="rounded-3xl bg-apricot-2 p-4"><h4 className="mb-2 text-[11px] font-bold tracking-[0.12em] text-apricot uppercase">{titles[1]}</h4><ul className="space-y-1.5 text-[13.5px] leading-snug">{cons.map((x, i) => <li key={i} className="flex gap-2"><span className="mt-2 size-1.5 shrink-0 rounded-full bg-apricot" />{x}</li>)}</ul></div>}
    </div>
  );
}
