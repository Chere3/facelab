# Biblioteca de métodos del protocolo

53 métodos no quirúrgicos en `methods.yaml`. El protocolo elige entre 4 y 16 según el nivel de intensidad (mantenimiento, mejora, glow-up) y justifica cada uno con la medida y el percentil que lo motiva. `tier` limita quién puede proponerse: `basic` en todos los niveles, `intensive` desde mejora, `professional` (botox, relleno) solo con percentil extremo y médico.

Evidencia: A ensayos controlados · B estudios observacionales · C principio óptico o consenso · D anecdótico.

| id | Método | Actúa sobre | Evidencia | Coste (USD) | Frecuencia | Horizonte | Tier |
|---|---|---|---|---|---|---|---|
| `retinoid_night` | Retinoide tópico nocturno (retinol 0,3–0,5 % o adapaleno 0,1 %) | skin_texture, fine_lines, pores, acne, uneven_tone | A | 15–40 / mes | noches alternas 2 semanas, luego cada noche | 8–12 semanas | basic |
| `sunscreen_daily` | Fotoprotector SPF 30–50 diario | uneven_tone, hyperpigmentation, fine_lines, skin_aging, redness | A | 10–25 / mes | cada mañana | inmediato (prevención), 3–6 meses (tono) | basic |
| `vitamin_c_am` | Sérum de vitamina C (10–15 % ácido L-ascórbico) por la mañana | uneven_tone, hyperpigmentation, dullness | B | 15–40 / mes | cada mañana antes del SPF | 8–12 semanas | basic |
| `niacinamide` | Niacinamida 4–5 % | pores, redness, uneven_tone, oiliness | B | 8–20 / mes | 1–2 veces al día | 4–8 semanas | basic |
| `azelaic_acid` | Ácido azelaico 10–15 % | redness, acne, hyperpigmentation | A | 12–30 / mes | 1–2 veces al día | 8–12 semanas | basic |
| `aha_bha_exfoliation` | Exfoliación química suave (ácido glicólico 5–8 % o salicílico 2 %) | skin_texture, pores, acne, dullness | B | 10–25 / mes | 2–3 veces por semana | 4–8 semanas | basic |
| `hydration_barrier` | Hidratante con ceramidas y protección de barrera | dryness, redness, skin_texture, lip_dryness | B | 8–25 / mes | 2 veces al día | 1–2 semanas | basic |
| `brow_shaping` | Perfilado de cejas según la forma natural (arco, cola, densidad) | brow_shape, brow_tilt, brow_symmetry, eye_framing | C | 15–35 por sesión | cada 3–5 semanas | inmediato | basic |
| `brow_growth_serum` | Densificación de cejas (minoxidil 2–5 % tópico bajo indicación, o sérum con péptidos) | brow_density, brow_thickness | B | 10–30 / mes | diario | 3–4 meses | basic |
| `lash_serum` | Sérum de pestañas (bimatoprost bajo indicación o péptidos) | lash_fullness, eye_framing | A | 20–60 / mes | cada noche | 8–16 semanas | basic |
| `under_eye_routine` | Rutina de ojeras: sueño, sal, cafeína tópica, retinoide suave, corrector de tono | under_eye_pigmentation, under_eye_puffiness, under_eye_hollowness | B | 10–40 / mes | diario | 6–10 semanas | basic |
| `haircut_face_shape` | Corte y volumen del pelo adaptados a la forma de cara y tercios | face_shape_balance, forehead_height, facial_thirds, face_width, jaw_balance | C | 20–60 por corte | cada 4–6 semanas | inmediato | basic |
| `beard_shaping` | Barba perfilada para redefinir mandíbula y mentón (si aplica) | jaw_definition, chin_projection, jaw_to_cheek, lower_third | B | 0–30 / mes | mantenimiento semanal | 4–8 semanas | basic |
| `body_fat_reduction` | Reducción moderada de grasa corporal (déficit calórico y fuerza) | jaw_definition, cheek_definition, submental_fat, facial_adiposity | A | 0 | diario | 3–6 meses | basic |
| `sleep_hygiene` | Sueño 7–9 h regular | under_eye_puffiness, skin_dullness, perceived_health, visual_age | A | 0 | diario | 1–2 semanas | basic |
| `sodium_alcohol` | Reducir sodio y alcohol para bajar retención facial | facial_puffiness, under_eye_puffiness, jaw_definition | B | 0 | diario | 1–3 semanas | basic |
| `posture_head` | Postura de cabeza y cuello (evitar cabeza adelantada) | jaw_definition, neck_definition, submental_angle, profile_convexity | C | 0 | diario | 2–4 semanas | basic |
| `teeth_whitening` | Blanqueamiento dental (peróxido de carbamida 10–16 % en férula) | tooth_color, smile_quality | A | 30–300 | 2 semanas, mantenimiento anual | 2 semanas | basic |
| `clear_aligners` | Alineadores transparentes (ortodoncia) | tooth_alignment, smile_symmetry, lip_support | A | 1500–5000 | 22 h/día | 6–18 meses | basic |
| `lip_care` | Cuidado labial: exfoliación suave, bálsamo con SPF, hidratación | lip_smoothness, lip_hydration, lip_lines | C | 5–15 / mes | diario | 1–2 semanas | basic |
| `glasses_frames` | Montura de gafas elegida por forma de cara y anchura de ojos | eye_spacing_ratio, face_width, brow_position, facial_fifths | C | 50–300 | una vez | inmediato | basic |
| `skin_hydration_water` | Hidratación sistémica e ingesta de agua adecuada | skin_texture, dullness | B | 0 | diario | 2–4 semanas | basic |
| `facial_massage_lymph` | Drenaje facial manual o gua sha (efecto temporal) | facial_puffiness, under_eye_puffiness | C | 0–40 | 5 min por la mañana | inmediato, temporal | basic |
| `dermatologist_referral` | Consulta dermatológica para acné activo, rosácea, melasma o cicatrices | acne, acne_scarring, redness, hyperpigmentation | A | 50–200 | según indicación | variable | basic |
| `photo_technique` | Técnica fotográfica: luz frontal difusa, cámara a la altura de los ojos, distancia focal ≥50 mm | perceived_nose_width, perceived_face_width, perceived_symmetry | B | 0 | siempre | inmediato | basic |
| `tranexamic_topical` | Ácido tranexámico tópico 2–5 % para manchas | hyperpigmentation, uneven_tone, melasma | B | 15–35 / mes | 1–2 veces al día | 8–12 semanas | basic |
| `benzoyl_peroxide` | Peróxido de benzoilo 2,5–5 % para acné inflamatorio | acne, redness | A | 8–15 / mes | 1 vez al día | 4–8 semanas | basic |
| `chemical_peel_pro` | Peeling químico profesional superficial (glicólico 30–50 % o salicílico 20–30 %) | skin_texture, acne_scarring, hyperpigmentation, dullness | A | 80–200 por sesión | cada 3–4 semanas, 4–6 sesiones | 3–4 meses | basic |
| `microneedling` | Microneedling profesional para cicatrices de acné y textura | acne_scarring, skin_texture, pores | A | 150–400 por sesión | cada 4–6 semanas, 3–4 sesiones | 3–6 meses | basic |
| `laser_vascular` | Láser vascular o IPL para rojez y capilares (dermatología) | redness, vascular_visibility | A | 150–400 por sesión | 2–4 sesiones | 2–4 meses | basic |
| `brow_lamination` | Laminado de cejas para orden y sensación de densidad | brow_density, brow_shape, brow_thickness | C | 40–90 por sesión | cada 6–8 semanas | inmediato | basic |
| `scalp_hair_care` | Cuidado capilar y volumen (minoxidil bajo indicación si hay pérdida) | hair_density, forehead_height, facial_thirds, face_framing | A | 15–40 / mes | diario | 4–6 meses | basic |
| `hydrafacial_cleansing` | Limpieza facial profesional periódica | pores, oiliness, dullness, skin_texture | C | 60–150 por sesión | cada 4–8 semanas | inmediato | basic |
| `oral_hygiene_gum` | Higiene bucal y revisión periodontal (encías, halitosis, esmalte) | smile_quality, gum_visibility, tooth_color | A | 50–120 / año | 2 veces al día; revisión semestral | 4–8 semanas | basic |
| `mewing_no` | Postura lingual (\"mewing\") como cambio óseo | jaw_definition | C | 0 | - | - | basic |
| `strength_training` | Entrenamiento de fuerza 2–3 veces por semana | perceived_health, posture, neck_definition, body_composition | A | 0–40 / mes | 2–3 sesiones / semana | 3–6 meses | basic |
| `smoking_alcohol_reduction` | Dejar de fumar y reducir alcohol | skin_aging, visual_age, redness, tooth_color, under_eye_puffiness | A | 0 | - | 3–12 meses | basic |
| `hat_uv_avoidance` | Sombra, gorra o sombrero y evitar el sol de mediodía | hyperpigmentation, skin_aging, redness | A | 0–30 | diario al aire libre | prevención | basic |
| `makeup_grooming_basics` | Corrección de tono y definición con maquillaje o grooming sutil (corrector, gel de cejas) | under_eye_pigmentation, uneven_tone, brow_density, lip_color_contrast | C | 10–40 | diario, opcional | inmediato | basic |
| `hair_transformation` | Transformación de pelo completa (corte con forma concreta, textura y producto) | face_shape_balance, facial_thirds, forehead_height, face_width, jaw_balance, first_impression | B | 40–120 por corte + 20–40 producto | cada 3–4 semanas | inmediato; 3–6 meses si hay que dejar crecer | intensive |
| `hair_color` | Cambio de color o tono de pelo para contrastar con la piel y los ojos | contrast, skin_tone_harmony, first_impression | C | 60–200 | cada 6–10 semanas | inmediato | intensive |
| `beard_growth_program` | Programa de barba: dejar crecer 8–12 semanas, minoxidil 5 % en zonas ralas bajo indicación, perfilado profesional | jaw_definition, chin_projection, jaw_to_cheek, lower_third, facial_masculinity | B | 20–40 / mes | diario; perfilado cada 2–3 semanas | 3 meses | intensive |
| `body_recomposition` | Recomposición corporal con objetivo numérico (déficit 400–500 kcal, 1,6–2 g proteína/kg, fuerza 3×/semana, 8–10 k pasos) | jaw_definition, cheek_definition, submental_fat, facial_adiposity, perceived_health, visual_age | A | 0–50 / mes | diario | 3–9 meses (0,5 kg/semana) | intensive |
| `skin_pro_program` | Programa dermatológico intensivo (retinoide con receta + 3–4 peelings o microneedling + láser vascular si hay rojez) | skin_texture, acne_scarring, hyperpigmentation, redness, pores, fine_lines, visual_age | A | 600–1500 en 6 meses | sesiones cada 4 semanas + rutina diaria | 6 meses | professional |
| `brow_redesign` | Rediseño de cejas (mapeo profesional; microblading o laminado si faltan densidad o forma) | brow_shape, brow_density, brow_position, eye_framing, brow_symmetry | C | 80–400 | microblading cada 12–18 meses; laminado cada 6–8 semanas | inmediato | intensive |
| `lash_lift_tint` | Lifting y tinte de pestañas | lash_fullness, eye_framing, eye_openness | C | 50–120 | cada 6–8 semanas | inmediato | intensive |
| `dental_full` | Plan dental completo (limpieza, blanqueamiento profesional, alineadores si hay apiñamiento, carillas solo si hay defectos) | tooth_color, tooth_alignment, smile_quality, lip_support | A | 300–5000 | según plan | 2 semanas (blanqueo) a 12–18 meses (alineadores) | professional |
| `eyewear_or_contacts` | Cambio de gafas (montura por forma de cara) o pasar a lentillas si las gafas ocultan ojos y cejas | eye_spacing_ratio, face_width, brow_position, facial_fifths, eye_framing | C | 50–300 | una vez | inmediato | intensive |
| `style_color_palette` | Paleta de color de ropa según subtono de piel, ojos y pelo; cuello y escote que favorezcan el tercio inferior | contrast, skin_tone_harmony, first_impression, neck_definition | C | 0–200 | una vez | inmediato | intensive |
| `posture_neck_program` | Programa de postura y cuello (chin tucks, extensión torácica, fuerza de espalda alta) | jaw_definition, neck_definition, submental_angle, profile_convexity, posture | B | 0 | 10 min diarios | 6–8 semanas | intensive |
| `botox_pro` | Toxina botulínica con médico (frente, entrecejo, patas de gallo; masetero si mandíbula muy ancha) | wrinkles, fine_lines, brow_position, jaw_width, visual_age | A | 200–600 por sesión | cada 3–4 meses | 2 semanas | professional |
| `filler_pro` | Ácido hialurónico con médico (mentón, mandíbula, ojeras o labios) cuando la deficiencia es clara | chin_projection, jaw_definition, under_eye_hollowness, lip_fullness, midface_ratio, facial_convexity | A | 400–1200 por zona | cada 9–18 meses | inmediato | professional |
| `sleep_recovery_program` | Sueño 7,5–9 h con horario fijo, sin pantallas 1 h antes, habitación oscura | under_eye_puffiness, skin_dullness, perceived_health, visual_age | A | 0 | diario | 2 semanas | intensive |
