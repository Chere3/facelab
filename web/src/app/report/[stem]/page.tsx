import { ReportView } from "@/components/report/ReportView";
import type { Report, Status } from "@/lib/types";

const API = process.env.FACELAB_API ?? "http://127.0.0.1:8766";

/** En modo impresión (?print=1) el informe se renderiza completo en el servidor: Chrome headless lo imprime sin esperar JS. */
export default async function ReportPage({ params, searchParams }: { params: Promise<{ stem: string }>; searchParams: Promise<{ print?: string }> }) {
  const { stem } = await params;
  const { print } = await searchParams;
  let initial: { report: Report | null; status: Status | null } | null = null;
  if (print === "1") {
    const [r, s] = await Promise.all([fetch(`${API}/api/report/${encodeURIComponent(stem)}`, { cache: "no-store" }), fetch(`${API}/api/status/${encodeURIComponent(stem)}`, { cache: "no-store" })]);
    initial = { report: r.ok ? await r.json() : null, status: s.ok ? await s.json() : null };
  }
  return <ReportView stem={stem} print={print === "1"} initial={initial} />;
}
