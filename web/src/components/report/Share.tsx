"use client";
import type { Report } from "@/lib/types";
import { storyCards } from "@/components/story/StoryCards";
import { Section, SectionHead } from "@/components/site/Section";

export function Share({ R, stem }: { R: Report; stem: string }) {
  const cards = storyCards(R);
  if (!cards.length) return null;
  return (
    <Section id="compartir" className="no-print">
      <SectionHead eyebrow="Para compartir" title={<>Tu informe <span className="gradient-text">en tarjetas.</span></>} lede="Formato vertical 9:16 listo para historias. Cada tarjeta se descarga como PNG a 1080×1920." />
      <div className="no-scrollbar mt-6 flex snap-x gap-4 overflow-x-auto pb-4">
        {cards.map((c, i) => (
          <div key={i} className="w-[270px] shrink-0 snap-start">
            <div className="h-[480px] w-[270px] overflow-hidden rounded-[26px] bg-paper shadow-lift"><div className="origin-top-left scale-[0.25]">{c}</div></div>
            <div className="mt-2.5 flex items-center justify-between text-[12px] text-muted-foreground"><span>Tarjeta {i + 1} de {cards.length}</span><a className="rounded-full btn-glow px-3 py-1.5 font-semibold" href={`/api/card/${stem}/${i}`} download>Descargar PNG</a></div>
          </div>
        ))}
      </div>
    </Section>
  );
}
