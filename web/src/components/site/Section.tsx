import { cn } from "@/lib/utils";

/** Cabecera de sección: eyebrow + titular serif + una frase. */
export function SectionHead({ eyebrow, title, lede, className, right }: { eyebrow?: string; title: React.ReactNode; lede?: React.ReactNode; className?: string; right?: React.ReactNode }) {
  return (
    <div className={cn("flex flex-col gap-4 md:flex-row md:items-end md:justify-between", className)}>
      <div>
        {eyebrow && <div className="eyebrow mb-2">{eyebrow}</div>}
        <h2 className="text-[clamp(28px,3.4vw,42px)] font-medium leading-[1.02]">{title}</h2>
        {lede && <div className="mt-3 max-w-[58ch] text-[16px] text-muted-foreground">{lede}</div>}
      </div>
      {right}
    </div>
  );
}

export function Section({ id, children, className }: { id?: string; children: React.ReactNode; className?: string }) {
  return <section id={id} className={cn("scroll-mt-32 pt-20 md:pt-24", className)}>{children}</section>;
}

export const Light = ({ children }: { children: React.ReactNode }) => <em className="font-light not-italic text-muted-foreground">{children}</em>;
export const Italic = ({ children }: { children: React.ReactNode }) => <em className="italic text-coral">{children}</em>;
