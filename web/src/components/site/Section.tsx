import { cn } from "@/lib/utils";

/** Cabecera compacta de panel: eyebrow + título + una frase. */
export function SectionHead({ eyebrow, title, lede, className, right }: { eyebrow?: string; title: React.ReactNode; lede?: React.ReactNode; className?: string; right?: React.ReactNode }) {
  return (
    <div className={cn("flex flex-col gap-3 md:flex-row md:items-end md:justify-between", className)}>
      <div>
        {eyebrow && <div className="eyebrow mb-1.5">{eyebrow}</div>}
        <h2 className="text-[clamp(22px,2.4vw,30px)] leading-[1.05]">{title}</h2>
        {lede && <div className="mt-2 max-w-[62ch] text-[14px] text-muted-foreground">{lede}</div>}
      </div>
      {right}
    </div>
  );
}

/** Cada sección del informe es un panel del dashboard. */
export function Section({ id, children, className }: { id?: string; children: React.ReactNode; className?: string }) {
  return <section id={id} className={cn("panel scroll-mt-24 p-5 md:p-7", className)}>{children}</section>;
}

export const Light = ({ children }: { children: React.ReactNode }) => <span className="font-light text-muted-foreground">{children}</span>;
export const Italic = ({ children }: { children: React.ReactNode }) => <span className="gradient-text">{children}</span>;
