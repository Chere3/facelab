"use client";
import type { Report } from "@/lib/types";
import { out } from "@/lib/api";
import { Sci, Simple, useMode } from "@/lib/mode";
import { Button } from "@/components/ui/button";
import { Section, SectionHead } from "@/components/site/Section";
import { Card, Cap, Photo } from "./bits";
import { MeasureRows, PlainMeasures } from "./MeasureRows";
import { Narrative } from "./Narrative";

export const ZONE_KEYS: Record<string, string[]> = {
  ojos: ["eye_aspect_ratio", "canthal_tilt", "eye_spacing_ratio", "brow_position", "brow_tilt", "eye_width", "eye_height", "intercanthal_width", "interpupillary_distance"],
  nariz: ["nasal_index", "nose_to_intercanthal", "sagittal_angles", "nose_width", "nasal_height"],
  boca: ["mouth_to_nose", "lip_ratio", "lip_height_to_mouth_width", "commissure_tilt", "mouth_width", "philtrum_length"],
  inferior: ["jaw_to_cheek", "chin_to_lower_face", "chin_width_to_jaw", "bigonial_width", "bizygomatic_width", "lower_face_height", "chin_height"],
};

export function Zone({ R, id, title, eyebrow, photo, lede, stepState, stepDetail }: { R: Report; id: string; title: React.ReactNode; eyebrow: string; photo: string; lede: string; stepState: (id: string) => string; stepDetail: (id: string) => string }) {
  const { setMode } = useMode();
  const annot = out(R.assets?.[photo]), plain = out(R.assets?.[photo.replace("_annot", "")]);
  return (
    <Section id={id}>
      <SectionHead eyebrow={eyebrow} title={title} lede={lede} />
      <div className="mt-6 grid gap-6 md:grid-cols-[minmax(0,5fr)_minmax(0,7fr)]">
        <div>
          <Photo src={annot} ratio="auto" fit="contain" className="rounded-3xl" />
          <Cap>Puntos y líneas de medida sobre tu foto.</Cap>
          <Sci className="mt-3 grid grid-cols-2 gap-3"><Photo src={plain} ratio="auto" fit="contain" /><Photo src={out(R.assets?.mesh)} ratio="auto" fit="contain" /></Sci>
        </div>
        <div className="space-y-4">
          <Simple><PlainMeasures R={R} keys={ZONE_KEYS[id]} /></Simple>
          <Sci><Card><MeasureRows R={R} keys={ZONE_KEYS[id]} /></Card></Sci>
          <Narrative R={R} k={id} state={stepState("narrative")} detail={stepDetail("narrative")} />
          <Simple className="no-print flex items-center gap-2 text-[12px] text-muted-foreground">Estás en modo simple. <Button variant="outline" size="sm" className="rounded-full" onClick={() => setMode("sci")}>Ver los datos de esta zona</Button></Simple>
        </div>
      </div>
    </Section>
  );
}
