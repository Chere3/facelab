import type { FeedItem, Report, ReportRow, Status } from "./types";

/* Todas las rutas son relativas: next.config.ts las reenvía a FastAPI. */
const j = async <T,>(r: Response): Promise<T> => { if (!r.ok) throw new Error((await r.json().catch(() => ({}))).error || r.statusText); return r.json(); };

export const out = (name?: string | null, v?: number) => (name ? `/out/${name}${v ? `?v=${v}` : ""}` : "");
export const getReport = (stem: string) => fetch(`/api/report/${stem}`, { cache: "no-store" }).then((r) => (r.ok ? (r.json() as Promise<Report>) : null));
export const getStatus = (stem: string) => fetch(`/api/status/${stem}`, { cache: "no-store" }).then((r) => (r.ok ? (r.json() as Promise<Status>) : null));
export const getFeed = () => fetch("/api/feed", { cache: "no-store" }).then((r) => j<FeedItem[]>(r));
export const getReports = () => fetch("/reports", { cache: "no-store" }).then((r) => j<ReportRow[]>(r));
export const regen = (stem: string, steps: string[], extra: { ambition?: string; look_ids?: string[] } = {}) =>
  fetch(`/api/regen/${stem}`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ steps, ...extra }) }).then((r) => j<{ ok: boolean }>(r));
export const putReview = (stem: string, patch: object) =>
  fetch(`/api/review/${stem}`, { method: "PUT", headers: { "Content-Type": "application/json" }, body: JSON.stringify(patch) }).then((r) => j<{ ok: boolean; review?: Report["review"] }>(r));
export const analyze = (fd: FormData) => fetch("/analyze", { method: "POST", body: fd }).then((r) => j<{ stem: string; report_url: string }>(r));
