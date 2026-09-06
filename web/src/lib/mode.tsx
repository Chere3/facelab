"use client";
import { createContext, useContext, useEffect, useSyncExternalStore } from "react";

/** Modo de lectura del informe: "simple" (para cualquiera) o "sci" (valores, percentiles y normas). */
export type Mode = "simple" | "sci";
const listeners = new Set<() => void>();
const subscribe = (l: () => void) => { listeners.add(l); return () => { listeners.delete(l); }; };
function read(): Mode {
  try {
    if (new URLSearchParams(window.location.search).get("print") === "1") return "sci";
    return localStorage.getItem("facelab.sci") === "1" ? "sci" : "simple";
  } catch { return "simple"; }
}
const Forced = createContext<Mode | null>(null);
/** Fuerza un modo en todo el subárbol (p. ej. "sci" al imprimir, donde no hay JS). */
export const ForceMode = Forced.Provider;
export function useMode() {
  const stored = useSyncExternalStore(subscribe, read, () => "simple" as Mode);
  const forced = useContext(Forced);
  const mode = forced ?? stored;
  const setMode = (m: Mode) => { try { localStorage.setItem("facelab.sci", m === "sci" ? "1" : "0"); } catch {} listeners.forEach((l) => l()); };
  return { mode, setMode };
}
export function ModeProvider({ children }: { children: React.ReactNode }) {
  const { mode } = useMode();
  useEffect(() => { document.documentElement.dataset.mode = mode; }, [mode]);
  return <>{children}</>;
}
type Wrap = { children: React.ReactNode; className?: string; as?: "div" | "span" };
export const Sci = ({ children, className = "", as: T = "div" }: Wrap) => <T className={`sci-only ${className}`}>{children}</T>;
export const Simple = ({ children, className = "", as: T = "div" }: Wrap) => <T className={`simple-only ${className}`}>{children}</T>;
