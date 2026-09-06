import Link from "next/link";
import { cn } from "@/lib/utils";

export function Logo({ className, size = 22 }: { className?: string; size?: number }) {
  return (
    <Link href="/" className={cn("inline-flex items-center gap-2 font-display tracking-tight text-ink no-underline", className)} style={{ fontSize: size * 0.85 }}>
      <span aria-hidden className="inline-block rounded-[30%]" style={{ width: size, height: size, background: "conic-gradient(from 200deg, #ff5c7a, #ffb27a, #f0b429, #8f6ff0, #ff5c7a)" }} />
      facelab
    </Link>
  );
}
