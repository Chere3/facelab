import { cn } from "@/lib/utils";

const TONES: Record<string, string> = {
  neutral: "bg-paper text-ink-2 border-line",
  ok: "bg-sage-2 text-sage border-sage/20",
  warn: "bg-apricot-2 text-apricot border-apricot/20",
  accent: "bg-coral-2 text-coral border-coral/20",
  lavender: "bg-lavender-2 text-lavender border-lavender/20",
  ink: "btn-glow border-ink",
};

export function Chip({ children, tone = "neutral", dot, className, size = "md" }: { children: React.ReactNode; tone?: keyof typeof TONES; dot?: string; className?: string; size?: "sm" | "md" | "lg" }) {
  return (
    <span className={cn("inline-flex items-center gap-1.5 rounded-full border font-semibold whitespace-nowrap", TONES[tone], size === "sm" ? "px-2.5 py-0.5 text-[11px]" : size === "lg" ? "px-4 py-2 text-[14px]" : "px-3 py-1 text-[12px]", className)}>
      {dot && <i className="inline-block size-2.5 rounded-full border border-white/10" style={{ background: dot }} />}
      {children}
    </span>
  );
}
