/* Tipos del informe (out/mine/<stem>.json). Laxos a propósito: el JSON crece paso a paso. */
export type Step = { id: string; label: string; state: "pending" | "running" | "done" | "error" | "skipped"; detail?: string };
export type Status = { steps: Step[]; current: string | null; done: boolean; error: string | null; updated: number };

export type Color = { hex: string; name: string };
export type Measure = { value: number | Record<string, number> | null; unit: string; caveat?: string; true?: Record<string, number>; detail?: { mean_error_pct_face_height?: number; score?: number; per_landmark_pct?: Record<string, number> } };
export type Norm = { percentile: number; group_mean?: number; group_sd?: number; z?: number };
export type Narr = { summary?: string; findings?: { measure: string; statement: string }[]; strengths?: string[]; watch?: string[]; error?: string };
export type Action = { method_id?: string; name: string; why?: string; spec?: string; cost?: string; frequency?: string; horizon?: string; difficulty?: string; evidence?: string };
export type Phase = { name: string; weeks?: string; goal?: string; actions?: Action[] };
export type Look = { id: string; name?: string; occasion?: string; expression?: "neutral" | "feminine" | "masculine"; pieces?: string[]; colors?: string[]; accessories?: string[]; grooming?: string; description?: string; maintenance?: string; why?: string };
export type Render = { file?: string; png?: string; kind?: string; prompt?: string; ts?: number; error?: string };

export interface Report {
  stem: string; source?: string; person?: string; date?: string; feed?: boolean;
  profile?: { sex?: string | null; ancestry?: string | null; age?: number | null; ambition?: string | null };
  quality?: { yaw_deg: number; pitch_deg: number; roll_deg: number; blur_laplacian_var: number };
  warnings: string[];
  measures: Record<string, Measure>;
  catalog: Record<string, { name: string; unit?: string; norm?: unknown }>;
  norms?: { group: string; n: number; per_measure: Record<string, Norm> };
  scores?: {
    symmetry?: { score: number; percentile: number; group_mean?: number };
    averageness?: { score: number; note?: string };
    dimorphism?: { masculinity_index: number; percentile_within_sex?: number | null; note?: string };
    proportionality?: { score: number; note?: string };
    global?: {
      composite?: { score: number; components: Record<string, number>; weights: Record<string, number>; notes: Record<string, string>; missing: string[]; method: string };
      model?: { predicted_rating: number; scale: string; percentile_in_group: number; group: string; n_group: number; group_human_mean: number; cv_r2: number; cv_r: number; n_train: number; note: string };
    };
  };
  assets?: Record<string, string>;
  age?: { visual_age: number; note?: string };
  skin?: { redness_pct: number; spots_pct: number; texture_index: number; shine_pct: number; tone_unevenness: number; skin_pixels?: number; note?: string; maps?: Record<string, string>; percentiles?: Record<string, { percentile: number; group_mean?: number } | string | number> };
  parsing?: { trichion_y?: number | null; hair_visible?: boolean; hat?: boolean; glasses?: boolean; ear_visible?: { any: boolean }; neck_visible?: boolean; forehead_height_px?: number; facial_thirds_true?: Record<string, number> };
  style?: {
    colors?: Record<string, { hex: string; L: number; chroma?: number; label?: string; depth?: string; undertone?: string } | null>;
    axes?: Record<string, number>;
    contrast?: { level: string; rule: string }; chroma?: string; note?: string;
    season?: { id: string; name: string; secondary?: string; margin?: number; ranking?: { id: string; name: string; score: number }[]; summary?: string; why?: string[] };
    palette?: { best: Color[]; neutrals: Color[]; avoid: Color[]; metals?: string; hair_colors?: string[]; makeup?: string[]; patterns?: string };
    face_shape?: { id: string; name: string; scores?: Record<string, number>; inputs?: Record<string, number>; note?: string };
    hair?: { visible: boolean; length?: string };
    bust?: string;
    shirts?: { mode: string; items: { hex: string; name: string; group: string; file: string }[] };
    renders?: Record<string, Render>;
    advice?: { summary?: string; color_story?: string; wardrobe?: { category: string; picks?: string[]; avoid?: string[] }[]; outfits?: Look[]; haircuts?: Look[]; grooming?: Look[]; hair_color?: string[]; avoid?: string[] };
  };
  profile_view?: { image?: string; measures?: Record<string, { value: number; range?: string; source?: string }>; warnings?: string[] };
  narrative?: Record<string, Narr>;
  protocol?: { intensity?: { tier?: string; computed?: string; requested?: string | null; drivers?: string[]; rationale?: string }; target_look?: string; phases?: Phase[]; expected_changes?: { measure: string; now?: string; target?: string; via?: string }[]; not_recommended?: string[]; letter?: string };
  visualization?: { model?: string; tier?: string; edits?: string[]; after?: string; after_3m?: string };
  review?: { approved?: boolean; by?: string; at?: string; notes?: string };
  json_path?: string;
}

export type FeedItem = { stem: string; name: string | null; date?: string; face?: string; profile?: Report["profile"]; global?: number | null; symmetry?: number | null; proportionality?: number | null; averageness?: number | null; visual_age?: number | null; season?: string | null; season_hex?: string | null; face_shape?: string | null; strength?: string; headline?: string | null; reviewed?: boolean; after?: string | null; look?: string | null };
export type ReportRow = { stem: string; profile?: Report["profile"]; face?: string; has_narrative: boolean; has_protocol: boolean; person?: string; date?: string; review?: Report["review"]; scores: Record<string, number | null> };
