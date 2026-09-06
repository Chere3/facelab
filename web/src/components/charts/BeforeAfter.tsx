"use client";
import { useState } from "react";
import { cn } from "@/lib/utils";

/** Comparador antes/después con slider. */
export function BeforeAfter({ before, after, className, labels = ["Antes", "Después"], ratio = "1/1" }: { before: string; after: string; className?: string; labels?: [string, string]; ratio?: string }) {
  const [v, setV] = useState(50);
  return (
    <div className={cn("relative overflow-hidden rounded-3xl bg-secondary", className)} style={{ aspectRatio: ratio }}>
      <img src={before} alt={labels[0]} className="absolute inset-0 size-full object-cover" />
      <div className="absolute inset-0 bg-cover bg-center" style={{ backgroundImage: `url('${after}')`, clipPath: `inset(0 0 0 ${v}%)` }} />
      <div className="pointer-events-none absolute inset-y-0 w-0.5 bg-white shadow-[0_0_0_1px_rgba(0,0,0,.15)]" style={{ left: `${v}%` }}>
        <span className="absolute top-1/2 left-1/2 flex size-9 -translate-x-1/2 -translate-y-1/2 items-center justify-center rounded-full bg-white text-[13px] text-ink shadow-lg">⇔</span>
      </div>
      <input type="range" min={0} max={100} value={v} onChange={(e) => setV(+e.target.value)} aria-label="comparar" className="absolute inset-0 m-0 size-full cursor-ew-resize opacity-0" />
      <span className="pointer-events-none absolute bottom-3 left-3 rounded-full bg-black/70 px-2.5 py-1 text-[10px] font-bold tracking-widest text-white uppercase">{labels[0]}</span>
      <span className="pointer-events-none absolute right-3 bottom-3 rounded-full bg-black/70 px-2.5 py-1 text-[10px] font-bold tracking-widest text-white uppercase">{labels[1]}</span>
    </div>
  );
}
