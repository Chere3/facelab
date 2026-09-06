"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { Logo } from "./Logo";
import { cn } from "@/lib/utils";

const LINKS = [["/", "Inicio"], ["/feed", "Feed"], ["/people", "Personas"], ["/admin", "Revisión"]] as const;

export function Nav({ children, cta = true }: { children?: React.ReactNode; cta?: boolean }) {
  const path = usePathname();
  return (
    <header className="no-print sticky top-0 z-30 glass border-b border-line">
      <div className="mx-auto flex max-w-[1240px] items-center gap-4 px-5 py-3 md:px-7">
        <Logo />
        {children}
        <nav className="ml-auto flex items-center gap-1 text-[13px] font-medium">
          {LINKS.map(([h, l]) => (
            <Link key={h} href={h} className={cn("hidden rounded-full px-3 py-1.5 text-muted-foreground transition hover:bg-secondary hover:text-ink sm:inline-block", (h === "/" ? path === "/" : path.startsWith(h)) && "text-ink")}>{l}</Link>
          ))}
          {cta && <Link href="/#analizar" className="ml-2 rounded-full btn-glow px-4 py-2 text-[13px] font-semibold transition hover:brightness-110">Analizar mi cara</Link>}
        </nav>
      </div>
    </header>
  );
}
