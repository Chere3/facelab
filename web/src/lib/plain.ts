/* Lenguaje llano: cómo se llama cada cosa y qué significa, para el modo simple. */
import type { Report } from "./types";

export const SEX: Record<string, string> = { male: "hombre", female: "mujer" };
export const ANC: Record<string, string> = { asian: "asiática", black: "negra", caucasian: "caucásica", hispanic: "hispana", indian: "india", mideastern: "medio-oriental", other: "mixta" };
export const SUB: Record<string, string> = { R: "derecho", L: "izquierdo", upper: "superior", middle: "medio", lower: "inferior", upper_proxy: "superior", outer_R: "sien derecha", outer_L: "sien izquierda", eye_R: "ojo derecho", eye_L: "ojo izquierdo", intercanthal: "entre ojos", nasofrontal: "nasofrontal", nasolabial: "nasolabial", mentolabial: "mentolabial" };
export const PROFILE_NAMES: Record<string, string> = { nasofrontal: "Ángulo nasofrontal", nasolabial: "Ángulo nasolabial", mentolabial: "Ángulo mentolabial", facial_convexity: "Convexidad facial (G–Sn–Pg)", total_convexity: "Convexidad total (G–Prn–Pg)", eline_upper_lip: "Labio superior a la línea E", eline_lower_lip: "Labio inferior a la línea E", chin_projection_ratio: "Proyección del mentón", nasal_projection_ratio: "Proyección nasal", gonial_soft: "Ángulo goniaco (tejido blando)", submental_cervical: "Ángulo submental-cervical" };
export const COMP: Record<string, string> = { averageness: "Armonía", dimorphism: "Rasgos", skin: "Piel", symmetry: "Simetría", proportionality: "Proporción", profile: "Perfil", visual_age: "Edad visual" };
export const COMP_SCI: Record<string, string> = { averageness: "Averageness", dimorphism: "Dimorfismo", skin: "Piel", symmetry: "Simetría", proportionality: "Proporcionalidad", profile: "Perfil", visual_age: "Edad visual" };

/** Nombre corto y en cristiano de cada medida, y qué significa estar alto o bajo. */
export const PLAIN: Record<string, { name: string; hi?: string; lo?: string; what?: string }> = {
  facial_thirds: { name: "Tercios de la cara", what: "frente, nariz y boca-mentón, a partes iguales según el canon" },
  facial_fifths: { name: "Quintos de la cara", what: "la cara dividida en cinco anchuras de ojo" },
  facial_index: { name: "Cara alargada o ancha", hi: "cara más alargada", lo: "cara más ancha" },
  fwhr: { name: "Anchura vs altura", hi: "cara más ancha que alta", lo: "cara más estrecha" },
  midface_ratio: { name: "Tercio medio", hi: "tercio medio más largo", lo: "tercio medio más corto" },
  eye_aspect_ratio: { name: "Ojos redondos o rasgados", hi: "ojos más abiertos y redondos", lo: "ojos más rasgados" },
  canthal_tilt: { name: "Inclinación de los ojos", hi: "ojos más ascendentes (efecto cat-eye)", lo: "ojos más rectos o descendentes" },
  eye_spacing_ratio: { name: "Separación de los ojos", hi: "ojos más separados", lo: "ojos más juntos" },
  brow_position: { name: "Altura de la ceja", hi: "cejas más altas sobre el ojo", lo: "cejas más pegadas al ojo" },
  brow_tilt: { name: "Arco de la ceja", hi: "cejas más rectas", lo: "cejas más arqueadas" },
  eye_width: { name: "Anchura del ojo" }, eye_height: { name: "Altura del ojo" }, intercanthal_width: { name: "Distancia entre ojos" }, interpupillary_distance: { name: "Distancia entre pupilas" }, biocular_width: { name: "Anchura biocular" },
  nasal_index: { name: "Anchura de la nariz", hi: "nariz más ancha que alta", lo: "nariz más fina y alargada" },
  nose_to_intercanthal: { name: "Nariz vs ojos", hi: "nariz más ancha que la separación de los ojos", lo: "nariz más estrecha que la separación de los ojos" },
  nose_width: { name: "Anchura de la nariz" }, nasal_height: { name: "Altura de la nariz" },
  sagittal_angles: { name: "Ángulos de perfil (estimados)" },
  mouth_to_nose: { name: "Boca vs nariz", hi: "boca ancha respecto a la nariz", lo: "boca pequeña respecto a la nariz" },
  lip_ratio: { name: "Labio superior vs inferior", hi: "labio superior más lleno", lo: "labio inferior más lleno" },
  lip_height_to_mouth_width: { name: "Grosor de labios", hi: "labios más gruesos", lo: "labios más finos" },
  commissure_tilt: { name: "Comisuras", hi: "comisuras hacia arriba", lo: "comisuras hacia abajo" },
  mouth_width: { name: "Anchura de la boca" }, philtrum_length: { name: "Filtrum" },
  jaw_to_cheek: { name: "Mandíbula vs pómulos", hi: "mandíbula tan ancha como los pómulos", lo: "mandíbula más estrecha que los pómulos" },
  chin_to_lower_face: { name: "Altura del mentón", hi: "mentón más alto", lo: "mentón más corto" },
  chin_width_to_jaw: { name: "Anchura del mentón", hi: "mentón más ancho", lo: "mentón más afilado" },
  bigonial_width: { name: "Anchura de mandíbula" }, bizygomatic_width: { name: "Anchura de pómulos" }, lower_face_height: { name: "Altura del tercio inferior" }, chin_height: { name: "Altura del mentón" },
  symmetry: { name: "Simetría", hi: "más simétrica", lo: "menos simétrica" },
};

/** Rango fijo de percentiles: 40–60 típico; 25–40 y 60–75 ligeramente; <25 y >75 claramente. */
export type Band = "lo" | "lo2" | "mid" | "hi2" | "hi";
export const band = (p: number | null | undefined): Band | null => (p == null ? null : p < 25 ? "lo" : p < 40 ? "lo2" : p <= 60 ? "mid" : p <= 75 ? "hi2" : "hi");
export const bandLabel: Record<Band, string> = { lo: "claramente por debajo", lo2: "algo por debajo", mid: "en la media", hi2: "algo por encima", hi: "claramente por encima" };
export const bandShort: Record<Band, string> = { lo: "bajo", lo2: "algo bajo", mid: "típico", hi2: "algo alto", hi: "alto" };
export const bandTone: Record<Band, "warn" | "ok" | "accent"> = { lo: "warn", lo2: "ok", mid: "ok", hi2: "ok", hi: "accent" };

/** Frase de una línea para una medida y su percentil, sin números. */
export function plainLine(id: string, p: number | null | undefined): string {
  const base = id.split(".")[0];
  const d = PLAIN[base];
  const b = band(p);
  if (!d) return "";
  if (!b) return d.what ? `${d.name}: ${d.what}` : d.name;
  if (b === "mid") return `${d.name}: en la media de tu grupo`;
  if ((b === "hi" || b === "hi2") && d.hi) return `${d.name}: ${d.hi}${b === "hi2" ? " (ligeramente)" : ""}`;
  if ((b === "lo" || b === "lo2") && d.lo) return `${d.name}: ${d.lo}${b === "lo2" ? " (ligeramente)" : ""}`;
  return `${d.name}: ${bandLabel[b]} de tu grupo`;
}

export const plainName = (id: string, catalog?: Report["catalog"]) => {
  if (PROFILE_NAMES[id]) return PROFILE_NAMES[id];
  const [b, k] = id.split(".");
  const n = PLAIN[b]?.name || catalog?.[b]?.name || b;
  return k ? `${n} · ${SUB[k] || k}` : n;
};
export const sciName = (id: string, catalog?: Report["catalog"]) => {
  if (PROFILE_NAMES[id]) return PROFILE_NAMES[id];
  const [b, k] = id.split(".");
  const n = catalog?.[b]?.name || PLAIN[b]?.name || b;
  return k ? `${n} · ${SUB[k] || k}` : n;
};

/** Percentil de una medida (media de sus subclaves si es compuesta). */
export function pctOf(R: Report, id: string): number | null {
  const pm = R.norms?.per_measure || {};
  if (pm[id]) return pm[id].percentile;
  const [b] = id.split(".");
  const m = R.measures?.[b];
  if (m && m.value && typeof m.value === "object") {
    const ks = Object.keys(m.value).map((k) => pm[`${b}.${k}`]).filter(Boolean);
    if (ks.length) return ks.reduce((a, x) => a + x.percentile, 0) / ks.length;
  }
  return null;
}

export const fmt = (v: unknown, n = 2): string => (typeof v === "number" ? (Number.isInteger(v) ? String(v) : v.toFixed(n)) : v == null ? "–" : String(v));
export const normText = (n: unknown): string => {
  if (!n || n === "none" || typeof n !== "object") return "";
  const o = n as Record<string, unknown>;
  const src = o.ranges && typeof o.ranges === "object" ? (o.ranges as Record<string, unknown>) : o;
  return Object.entries(src).filter(([k]) => k !== "source").map(([k, v]) => `${k} ${String(v)}`).join(" · ");
};

/** Puntos fuertes y a vigilar, uno por sección, para el resumen. */
export function highlights(R: Report, n = 4) {
  const s: string[] = [], w: string[] = [];
  for (const v of Object.values(R.narrative || {})) { (v.strengths || []).slice(0, 1).forEach((x) => s.push(x)); (v.watch || []).slice(0, 1).forEach((x) => w.push(x)); }
  return { strengths: s.slice(0, n), watch: w.slice(0, n) };
}

/** Los tres o cuatro datos que definen a la persona en una frase cada uno (hero del modo simple). */
export function headlineChips(R: Report): { label: string; hex?: string; tone?: string }[] {
  const out: { label: string; hex?: string; tone?: string }[] = [];
  const st = R.style, sc = R.scores;
  if (st?.season) out.push({ label: st.season.name, hex: st.palette?.best?.[0]?.hex });
  if (st?.face_shape) out.push({ label: `Cara ${st.face_shape.name.toLowerCase()}` });
  if (sc?.symmetry) { const b = band(sc.symmetry.percentile); if (b === "hi" || b === "hi2") out.push({ label: "Muy simétrica", tone: "ok" }); }
  if (st?.contrast) out.push({ label: `Contraste ${st.contrast.level}` });
  if (R.age) out.push({ label: `Edad visual ${R.age.visual_age}` });
  return out.slice(0, 4);
}

export const TIER: Record<string, { name: string; blurb: string }> = {
  mantenimiento: { name: "Mantener", blurb: "Tu base es sólida: rutina ligera para conservarla." },
  mejora: { name: "Mejorar", blurb: "Unas pocas cosas claras que cambiar en seis meses." },
  "glow-up": { name: "Glow-up", blurb: "Plan de doce meses: piel, pelo, cejas, cuerpo y ropa." },
};
export const DIFF: Record<string, string> = { easy: "fácil", medium: "esfuerzo medio", hard: "exigente" };
export const costLabel = (c?: string) => (!c ? "" : /^0\s*(€|\$)?$/.test(c.trim()) ? "gratis" : c);
export const EVIDENCE: Record<string, string> = { A: "evidencia sólida", B: "buena evidencia", C: "evidencia limitada", D: "opinión de expertos" };

/** Modo simple: quita paréntesis con cifras y traduce la jerga más habitual de la narrativa clínica. */
const JARGON: [RegExp, string][] = [
  [/\bFWHR\b/g, "anchura frente a altura de la cara"], [/\bratio\b/gi, "proporción"], [/\btilt cantal\b/gi, "inclinación de los ojos"], [/\bcantal\b/gi, "de los ojos"],
  [/\bintercantal\b/gi, "entre los ojos"], [/\bbigonial\b/gi, "de mandíbula"], [/\bbizigomátic[ao]\b/gi, "de pómulos"], [/\bmesoprosópic[ao]\b/gi, "de proporción media"],
  [/\bleptoprosópic[ao]\b/gi, "alargada"], [/\beuriprosópic[ao]\b/gi, "ancha"], [/\bmesorrin[ao]\b/gi, "de anchura media"], [/\bnasofrontal\b/gi, "entre frente y nariz"], [/\bnasolabial\b/gi, "entre nariz y labio"],
  [/\bmentolabial\b/gi, "entre labio y mentón"], [/\bgrupo de referencia\b/gi, "tu grupo"], [/\bpercentil típico\b/gi, "zona típica"], [/\bdimorfismo de forma\b/gi, "rasgos más marcados"],
  [/\baverageness\b/gi, "armonía"], [/\bproporcionalidad\b/gi, "proporción"], [/\bfiltrum\b/gi, "espacio entre nariz y labio"], [/\blandmarks?\b/gi, "puntos de la cara"], [/\bsegmentación\b/gi, "detección"],
];
export function simplify(t: string): string {
  let s = t.replace(/\b([a-z]+(?:_[a-z0-9]+)+)\b/g, (m) => PLAIN[m]?.name.toLowerCase() ?? m.replace(/_/g, " ")).replace(/\s*\([^()]*\d[^()]*\)/g, "").replace(/\s*\[[^\]]*\d[^\]]*\]/g, "");
  for (const [re, w] of JARGON) s = s.replace(re, w);
  s = s.replace(/\s{2,}/g, " ").replace(/\s+([,.;:])/g, "$1").replace(/,\s*\./g, ".").trim();
  return s.charAt(0).toUpperCase() + s.slice(1);
}
