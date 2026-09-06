"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import { analyze } from "@/lib/api";
import { Dialog, DialogContent, DialogTitle } from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Switch } from "@/components/ui/switch";
import { cn } from "@/lib/utils";

type F = { sex: string; ancestry: string; age: string; person: string; ambition: string; feed: boolean; file: File | null; pfile: File | null };
const N = 5;
const ANC = [["hispanic", "Hispana / latina"], ["caucasian", "Caucásica"], ["asian", "Asiática"], ["black", "Negra"], ["indian", "India"], ["mideastern", "Medio Oriente"], ["other", "Mixta / otra"]];

function Opt({ on, onClick, title, sub, pill }: { on: boolean; onClick: () => void; title: string; sub?: string; pill?: boolean }) {
  return <button type="button" onClick={onClick} className={cn("border-[1.5px] text-left transition", pill ? "rounded-full px-3.5 py-2" : "rounded-2xl p-3.5", on ? "border-coral bg-coral-2" : "border-line hover:border-line-2")}><b className="block text-[14px]">{title}</b>{sub && <small className="mt-0.5 block text-[12px] text-muted-foreground">{sub}</small>}</button>;
}
const Label = ({ children }: { children: React.ReactNode }) => <label className="mb-1.5 block text-[11px] font-bold tracking-[0.06em] text-muted-foreground uppercase">{children}</label>;

export function Onboarding({ open, onOpenChange }: { open: boolean; onOpenChange: (o: boolean) => void }) {
  const router = useRouter();
  const [step, setStep] = useState(0);
  const [F, setF] = useState<F>({ sex: "", ancestry: "", age: "", person: "", ambition: "", feed: true, file: null, pfile: null });
  const [preview, setPreview] = useState<string | null>(null);
  const [err, setErr] = useState("");
  const [busy, setBusy] = useState(false);
  const [prevOpen, setPrevOpen] = useState(open);
  if (open !== prevOpen) { setPrevOpen(open); if (open) { setStep(0); setErr(""); } }
  const set = <K extends keyof F>(k: K, v: F[K]) => {
    setF((f) => ({ ...f, [k]: v }));
    if (k === "file") { setPreview((old) => { if (old) URL.revokeObjectURL(old); return v ? URL.createObjectURL(v as File) : null; }); }
  };

  const submit = async () => {
    setBusy(true); setErr("");
    const fd = new FormData();
    if (F.file) fd.append("file", F.file);
    fd.append("sex", F.sex); fd.append("ancestry", F.ancestry); fd.append("age", F.age); fd.append("person", F.person); fd.append("ambition", F.ambition); fd.append("feed", F.feed ? "1" : "0");
    if (F.pfile) fd.append("profile_photo", F.pfile);
    try { const j = await analyze(fd); router.push(j.report_url); } catch (e) { setErr((e as Error).message); setBusy(false); }
  };
  const next = () => { if (step === 2 && !F.file) return setErr("Necesitamos la foto para seguir"); setErr(""); if (step === N - 1) return submit(); setStep((s) => Math.min(N - 1, s + 1)); };

  const steps = [
    <><div className="eyebrow">Hola 👋</div><h2 className="text-[32px] font-medium">Esto es lo que vamos a hacer</h2><p className="mt-1 mb-5 text-muted-foreground">En cinco minutos tendrás un informe completo de tu cara. Sin trucos, sin notas de belleza.</p>
      <div className="grid gap-2">{[["1 · Medimos", "478 puntos sobre tu foto y 32 proporciones, piel y colores."], ["2 · Comparamos", "Con personas de tu mismo sexo y ascendencia. Cada dato con su percentil."], ["3 · Te lo explicamos", "Qué juega a tu favor, qué colores y cortes te van, tu rutina y cómo te verías."]].map(([t, s]) => <div key={t} className="rounded-2xl border-[1.5px] border-coral bg-coral-2 p-3.5"><b className="block text-[14px]">{t}</b><small className="text-[12px] text-muted-foreground">{s}</small></div>)}</div></>,
    <><div className="eyebrow">Paso 1 de 4</div><h2 className="text-[32px] font-medium">Cuéntanos de ti</h2><p className="mt-1 mb-5 text-muted-foreground">Solo para compararte con gente parecida a ti. Puedes dejar cualquier campo en blanco.</p>
      <div className="space-y-4">
        <div><Label>Nombre o apodo</Label><Input placeholder="Cómo quieres aparecer en tu informe" value={F.person} onChange={(e) => set("person", e.target.value)} className="h-11 rounded-2xl" /></div>
        <div><Label>Sexo</Label><div className="grid grid-cols-3 gap-2"><Opt on={F.sex === "male"} onClick={() => set("sex", "male")} title="Hombre" /><Opt on={F.sex === "female"} onClick={() => set("sex", "female")} title="Mujer" /><Opt on={F.sex === ""} onClick={() => set("sex", "")} title="Prefiero no decirlo" sub="usa normas de todo el grupo" /></div></div>
        <div><Label>Ascendencia (grupo de referencia)</Label><div className="flex flex-wrap gap-2">{ANC.map(([v, l]) => <Opt key={v} pill on={F.ancestry === v} onClick={() => set("ancestry", v)} title={l} />)}</div></div>
        <div className="max-w-[160px]"><Label>Edad</Label><Input type="number" min={10} max={99} placeholder="años" value={F.age} onChange={(e) => set("age", e.target.value)} className="h-11 rounded-2xl" /></div>
      </div></>,
    <><div className="eyebrow">Paso 2 de 4</div><h2 className="text-[32px] font-medium">Tu foto de frente</h2><p className="mt-1 mb-5 text-muted-foreground">La mejor foto es la más aburrida: luz de día, cara relajada, mirando a cámara.</p>
      <label className="flex min-h-[190px] cursor-pointer flex-col items-center justify-center gap-1.5 rounded-3xl border-2 border-dashed border-coral/40 bg-secondary p-6 text-center transition hover:bg-coral-2" onDragOver={(e) => e.preventDefault()} onDrop={(e) => { e.preventDefault(); const f = e.dataTransfer.files[0]; if (f) set("file", f); }}>
        {preview ? <img src={preview} alt="" className="max-h-[220px] rounded-2xl" /> : <><b>Arrastra tu foto aquí o toca para elegirla</b><span className="text-[12px] text-muted-foreground">JPG o PNG · se queda en este ordenador</span></>}
        <input type="file" accept="image/*" hidden onChange={(e) => set("file", e.target.files?.[0] ?? null)} />
      </label>
      <div className="mt-3 grid grid-cols-2 gap-2 text-[13px] text-muted-foreground">{["Luz natural, sin sombras duras", "Sin gafas ni gorro", "Boca cerrada, sin sonreír", "Sin filtros ni retoques"].map((t) => <div key={t} className="flex gap-2"><span className="font-bold text-coral">✓</span>{t}</div>)}</div>
      <div className="mt-4"><Label>Foto de perfil (opcional, de lado, 90°)</Label><input type="file" accept="image/*" className="text-[13px]" onChange={(e) => set("pfile", e.target.files?.[0] ?? null)} /><p className="mt-1 text-[12px] text-muted-foreground">Con ella medimos los ángulos reales de nariz, labios y mentón.</p></div></>,
    <><div className="eyebrow">Paso 3 de 4</div><h2 className="text-[32px] font-medium">¿Cuánto quieres cambiar?</h2><p className="mt-1 mb-5 text-muted-foreground">El plan se adapta a tu ambición. Nunca proponemos cirugía.</p>
      <div className="grid gap-2 sm:grid-cols-3"><Opt on={F.ambition === ""} onClick={() => set("ambition", "")} title="Que decida el análisis" sub="según lo que encuentre" /><Opt on={F.ambition === "mejora"} onClick={() => set("ambition", "mejora")} title="Mejorar" sub="7–10 acciones, 6 meses" /><Opt on={F.ambition === "glow-up"} onClick={() => set("ambition", "glow-up")} title="Glow-up" sub="11–16 acciones, 12 meses: pelo, cejas, cuerpo, dientes, ropa" /></div></>,
    <><div className="eyebrow">Paso 4 de 4</div><h2 className="text-[32px] font-medium">Privacidad y listo</h2><p className="mt-1 mb-5 text-muted-foreground">Tu foto y tu informe se procesan y se guardan en este ordenador. Nada sale a internet salvo el texto que redacta la IA.</p>
      <label className="flex items-center gap-3 text-[14px]"><Switch checked={F.feed} onCheckedChange={(v) => set("feed", !!v)} />Mostrar mi resultado en el feed de personas</label>
      <div className="mt-4 rounded-2xl border-[1.5px] border-coral bg-coral-2 p-3.5"><b className="block text-[14px]">Resumen</b><small className="text-[12px] text-muted-foreground">{F.person || "Sin nombre"} · {({ male: "hombre", female: "mujer" } as Record<string, string>)[F.sex] || "sin sexo"} · {F.ancestry || "sin ascendencia"} · {F.age ? `${F.age} años` : "sin edad"} · ambición {F.ambition || "automática"} · {F.file ? F.file.name : "sin foto ⚠"}</small></div></>,
  ];

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-h-[calc(100vh-40px)] w-[min(720px,calc(100vw-24px))] overflow-auto rounded-[30px] p-7 sm:max-w-[720px] sm:p-9">
        <DialogTitle className="sr-only">Analizar mi cara</DialogTitle>
        <div className="mb-4 flex gap-1.5">{Array.from({ length: N }).map((_, i) => <i key={i} className={cn("h-1.5 flex-1 rounded-full", i <= step ? "bg-coral" : "bg-secondary")} />)}</div>
        {steps[step]}
        {err && <div className="mt-3 rounded-2xl bg-[#fbe3e0] px-3.5 py-2.5 text-[13px] text-destructive">{err}</div>}
        <div className="mt-6 flex items-center justify-between gap-3">
          <Button variant="outline" className={cn("rounded-full", !step && "invisible")} onClick={() => setStep((s) => Math.max(0, s - 1))}>Atrás</Button>
          <Button className="rounded-full" onClick={next} disabled={busy}>{busy ? "Subiendo…" : step === 0 ? "Empezar" : step === N - 1 ? "Analizar mi cara" : "Siguiente"}</Button>
        </div>
      </DialogContent>
    </Dialog>
  );
}
