"use client";
import { useEffect, useState } from "react";
import Link from "next/link";
import { getFeed, out } from "@/lib/api";
import type { FeedItem } from "@/lib/types";
import { SEX, simplify } from "@/lib/plain";
import { Nav } from "@/components/site/Nav";
import { Footer } from "@/components/site/Footer";
import { cn } from "@/lib/utils";

export default function FeedPage() {
  const [l, setL] = useState<FeedItem[] | null>(null);
  const [stories, setStories] = useState(false);
  useEffect(() => { getFeed().then(setL).catch(() => setL([])); }, []);
  return (
    <>
      <Nav />
      <main className={cn("mx-auto max-w-[1240px] px-5 md:px-7", stories && "max-w-none px-0")}>
        {!stories && <div className="flex flex-wrap items-end justify-between gap-4 pt-10 pb-3">
          <div><div className="eyebrow mb-2">Feed</div><h1 className="text-[clamp(30px,3.6vw,46px)] font-medium">Personas que ya <em className="italic text-coral">se analizaron.</em></h1><p className="mt-2 max-w-[60ch] text-muted-foreground">Cada tarjeta resume un informe real: lectura global, estación de color, forma de cara y lo que juega a su favor.</p></div>
          <Tabs on={stories} set={setStories} />
        </div>}
        {stories && <div className="fixed top-[68px] right-4 z-20"><Tabs on={stories} set={setStories} /></div>}
        {l == null ? <div className="mt-5 grid gap-4 md:grid-cols-3">{[0, 1, 2].map((i) => <div key={i} className="sk aspect-[9/16] rounded-[28px]" />)}</div>
          : !l.length ? <div className="mt-5 rounded-3xl border border-dashed border-line-2 p-10 text-center text-muted-foreground">Aún no hay análisis. <Link href="/#analizar" className="font-semibold text-coral">Sé la primera persona.</Link></div>
          : <div className={cn(stories ? "h-[calc(100vh-60px)] snap-y snap-mandatory overflow-y-auto" : "mt-5 grid gap-4 md:grid-cols-3")}>{l.map((x) => <FeedCard key={x.stem} x={x} story={stories} />)}</div>}
      </main>
      {!stories && <Footer />}
    </>
  );
}

function Tabs({ on, set }: { on: boolean; set: (v: boolean) => void }) {
  return <span className="inline-flex gap-0.5 rounded-full bg-secondary p-1 shadow-soft">{[["Rejilla", false], ["Historias", true]].map(([l, v]) => <button key={String(l)} onClick={() => set(v as boolean)} className={cn("rounded-full px-3.5 py-1.5 text-[13px] font-semibold", on === v ? "bg-paper text-ink shadow-soft" : "text-muted-foreground")}>{l}</button>)}</span>;
}

export function FeedCard({ x, story }: { x: FeedItem; story?: boolean }) {
  return (
    <Link href={`/report/${x.stem}`} className={cn("relative block overflow-hidden bg-secondary text-white shadow-soft", story ? "mx-auto h-[calc(100vh-60px)] max-w-[560px] snap-start" : "aspect-[9/16] rounded-[28px]")}>
      {x.face && <img src={out(x.face)} alt="" className="absolute inset-0 size-full object-cover" />}
      <div className="absolute top-3.5 right-3.5 left-3.5 flex items-center justify-between gap-2">
        <span className="flex items-center gap-2 rounded-full bg-ink/55 py-1.5 pr-3 pl-1.5 text-[13px] font-semibold backdrop-blur"><span className="flex size-6 items-center justify-center rounded-full bg-coral text-[11px]">{(x.name || "?")[0].toUpperCase()}</span>{x.name || "Anónimo"}</span>
        {x.global != null && <span className="rounded-full bg-paper px-3 py-1.5 text-[14px] font-bold text-ink">{x.global}<small className="ml-1 font-medium text-muted-foreground">/100</small></span>}
      </div>
      <div className="absolute right-0 bottom-0 left-0 bg-gradient-to-t from-ink/90 via-ink/60 to-transparent p-5 pt-16">
        <h3 className={cn("font-display font-medium leading-tight", story ? "text-[30px]" : "text-[22px]")}>{x.headline || "Análisis facial"}</h3>
        <p className={cn("mt-1.5 mb-2.5 opacity-90", story ? "text-[15px]" : "text-[13px]")}>{x.strength ? simplify(x.strength) : ""}</p>
        <div className="flex flex-wrap gap-1.5 text-[11px] font-semibold">
          {x.season && <span className="inline-flex items-center gap-1.5 rounded-full bg-white/15 px-2.5 py-1 backdrop-blur"><i className="size-2 rounded-full" style={{ background: x.season_hex || "#fff" }} />{x.season}</span>}
          {x.face_shape && <span className="rounded-full bg-white/15 px-2.5 py-1 backdrop-blur">Cara {x.face_shape.toLowerCase()}</span>}
          {x.visual_age && <span className="rounded-full bg-white/15 px-2.5 py-1 backdrop-blur">Edad visual {x.visual_age}</span>}
          {x.profile && <span className="rounded-full bg-white/15 px-2.5 py-1 backdrop-blur">{[SEX[x.profile.sex ?? ""], x.profile.age ? `${x.profile.age} años` : ""].filter(Boolean).join(" · ")}</span>}
        </div>
        <div className="mt-3 flex gap-3">{([["Simetría", x.symmetry], ["Proporción", x.proportionality], ["Armonía", x.averageness]] as const).filter((b) => b[1] != null).map(([k, v]) => <div key={k} className="flex-1"><small className="text-[10px] tracking-wider uppercase opacity-80">{k}</small><b className="block text-[16px]">{v}</b><i className="mt-1 block h-1 overflow-hidden rounded-full bg-white/25"><span className="block h-full bg-white" style={{ width: `${v}%` }} /></i></div>)}</div>
      </div>
      {x.reviewed && <span className="absolute right-3.5 bottom-3.5 rounded-full bg-sage-2 px-2 py-1 text-[10px] font-bold text-sage">Revisado</span>}
    </Link>
  );
}
