import type { Metadata } from "next";
import { Fraunces, Figtree, JetBrains_Mono } from "next/font/google";
import "./globals.css";
import { ModeProvider } from "@/lib/mode";
import { TooltipProvider } from "@/components/ui/tooltip";

const fraunces = Fraunces({ variable: "--font-fraunces", subsets: ["latin"], axes: ["SOFT", "WONK", "opsz"], style: ["normal", "italic"] });
const figtree = Figtree({ variable: "--font-figtree", subsets: ["latin"] });
const mono = JetBrains_Mono({ variable: "--font-jetbrains", subsets: ["latin"], weight: ["400", "500"] });

export const metadata: Metadata = {
  title: "facelab · tu cara, medida y explicada",
  description: "Análisis facial explicado para cualquiera: proporciones, colores, piel, rutina y looks sobre tu propia foto.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="es" className={`${fraunces.variable} ${figtree.variable} ${mono.variable} h-full`} suppressHydrationWarning>
      <body className="min-h-full flex flex-col">
        <ModeProvider>
          <TooltipProvider>{children}</TooltipProvider>
        </ModeProvider>
      </body>
    </html>
  );
}
