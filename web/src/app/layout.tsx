import type { Metadata } from "next";
import { Outfit, Manrope, JetBrains_Mono } from "next/font/google";
import "./globals.css";
import { ModeProvider } from "@/lib/mode";
import { TooltipProvider } from "@/components/ui/tooltip";

const outfit = Outfit({ variable: "--font-outfit", subsets: ["latin"] });
const manrope = Manrope({ variable: "--font-manrope", subsets: ["latin"] });
const mono = JetBrains_Mono({ variable: "--font-jetbrains", subsets: ["latin"], weight: ["400", "500"] });

export const metadata: Metadata = {
  title: "facelab · tu cara, medida y explicada",
  description: "Análisis facial explicado para cualquiera: proporciones, colores, piel, rutina y looks sobre tu propia foto.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="es" className={`${outfit.variable} ${manrope.variable} ${mono.variable} h-full`} suppressHydrationWarning>
      <body className="min-h-full flex flex-col">
        <ModeProvider>
          <TooltipProvider>{children}</TooltipProvider>
        </ModeProvider>
      </body>
    </html>
  );
}
