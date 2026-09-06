import type { Report } from "@/lib/types";
import { storyCards } from "@/components/story/StoryCards";

const API = process.env.FACELAB_API ?? "http://127.0.0.1:8766";

/** Tarjetas 9:16, renderizadas en el servidor (Chrome headless las captura sin esperar JS).
 *  ?card=n muestra solo una a 1080×1920. */
export default async function StoryPage({ params, searchParams }: { params: Promise<{ stem: string }>; searchParams: Promise<{ card?: string }> }) {
  const { stem } = await params;
  const { card } = await searchParams;
  const r = await fetch(`${API}/api/report/${encodeURIComponent(stem)}`, { cache: "no-store" });
  if (!r.ok) return <div className="p-10 text-muted-foreground">Este informe no existe.</div>;
  const R = (await r.json()) as Report;
  const cards = storyCards(R);
  if (card != null) return <div data-ready="1" style={{ width: 1080, height: 1920, overflow: "hidden" }}>{cards[+card] ?? cards[0]}</div>;
  return (
    <div className="flex flex-col items-center gap-10 p-10">
      {cards.map((c, i) => <div key={i} className="h-[960px] w-[540px] overflow-hidden rounded-[28px] shadow-lift"><div className="origin-top-left scale-50">{c}</div></div>)}
    </div>
  );
}
