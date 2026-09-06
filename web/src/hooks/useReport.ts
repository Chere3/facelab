"use client";
import { useCallback, useEffect, useRef, useState } from "react";
import { getReport, getStatus } from "@/lib/api";
import type { Report, Status } from "@/lib/types";

/** Informe progresivo: consulta estado + JSON cada 2,5 s hasta que el pipeline termina. */
export type Initial = { report: Report | null; status: Status | null } | null;
export function useReport(stem: string, initial: Initial = null) {
  const [report, setReport] = useState<Report | null>(initial?.report ?? null);
  const [status, setStatus] = useState<Status | null>(initial?.status ?? null);
  const [missing, setMissing] = useState(false);
  const polling = useRef(!(initial?.status?.done));
  const timer = useRef<ReturnType<typeof setTimeout> | null>(null);
  const tickRef = useRef<() => void>(() => {});

  const tick = useCallback(async () => {
    try {
      const [s, r] = await Promise.all([getStatus(stem), getReport(stem)]);
      setStatus(s); if (r) { setReport(r); setMissing(false); } else if (!s) setMissing(true);
      polling.current = !(s && s.done);
    } catch { /* red o JSON a medias: se reintenta */ }
    if (timer.current) clearTimeout(timer.current);
    if (polling.current) timer.current = setTimeout(() => tickRef.current(), 2500);
  }, [stem]);

  useEffect(() => { tickRef.current = tick; }, [tick]);
  useEffect(() => { if (!polling.current) return; const t = setTimeout(() => tickRef.current(), 0); return () => { clearTimeout(t); if (timer.current) clearTimeout(timer.current); }; }, [stem]);
  const wake = useCallback(() => { polling.current = true; tick(); }, [tick]);
  const stepState = (id: string) => status?.steps.find((s) => s.id === id)?.state ?? "pending";
  const stepDetail = (id: string) => status?.steps.find((s) => s.id === id)?.detail ?? "";
  return { report, status, missing, wake, stepState, stepDetail };
}
