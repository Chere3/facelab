# Catálogo de medidas

Las 32 medidas que calcula `measures.py`, con la fórmula sobre los puntos de `points.py`, la unidad y la norma citada. Las de `px` no se comparan entre personas; las marcadas como orientativas dependen de la profundidad estimada por MediaPipe.

| id | Medida | Fórmula | Unidad | Norma / fuente |
|---|---|---|---|---|
| `facial_thirds` | Tercios faciales |  | fraction | ideal: ≈0.33 cada uno; source: canon neoclásico; Farkas 1985 encontró tercio inferior algo mayor |
| `facial_fifths` | Quintos faciales |  | fraction | ideal: ≈0.20 cada uno; ojo ≈ intercantal; source: canon neoclásico; Farkas 1985 |
| `facial_index` | Índice facial morfológico | (nasion→menton) / (zygion R→L) × 100 | index | ranges: {'hypereuryprosopic': '<80', 'euryprosopic': '80–84.9', 'mesoprosopic': '85–89.9', 'leptoprosopic': '90–94.9', 'hyperleptoprosopic': '≥95'}; source: Martin & Saller (índice n-gn/zy-zy) |
| `fwhr` | Ratio anchura/altura facial (FWHR) | bizigomático / (párpado superior medio → labiale superius) | ratio | mean_male: 1.9; mean_female: 1.85; sd: 0.12; source: Carré & McCormick 2008; Lefevre et al. 2012 (aprox.) |
| `intercanthal_width` | Distancia intercantal |  | px | — |
| `interpupillary_distance` | Distancia interpupilar |  | px | — |
| `biocular_width` | Anchura biocular (exocantion a exocantion) |  | px | — |
| `eye_width` | Anchura de ojo (fisura palpebral) R/L |  | px | — |
| `eye_height` | Altura de fisura palpebral R/L |  | px | — |
| `eye_aspect_ratio` | Ratio altura/anchura del ojo (almendrado) |  | ratio | typical: 0.28–0.36; source: Farkas: fisura 30–31 mm × 10–11 mm ≈ 0.33 (aprox.) |
| `canthal_tilt` | Tilt cantal R/L | ángulo del eje exocantion–endocantion respecto a la horizontal; + = canto externo más alto | deg | typical: +2 a +6; sd: 3; source: Bashour 2006; Rhee et al. 2012 (aprox.) |
| `eye_spacing_ratio` | Ratio de separación ocular | intercantal / anchura media de ojo | ratio | ideal: 1.0; typical: 0.9–1.15; source: canon neoclásico; Farkas |
| `nose_width` | Anchura nasal (alar) |  | px | — |
| `nasal_height` | Altura nasal (nasion→subnasale) |  | px | — |
| `nasal_index` | Índice nasal | anchura alar / altura nasal × 100 | index | ranges: {'leptorrhine': '<70', 'mesorrhine': '70–84.9', 'platyrrhine': '85–99.9', 'hyperplatyrrhine': '≥100'}; source: Martin & Saller; Farkas |
| `nose_to_intercanthal` | Anchura nasal / intercantal |  | ratio | ideal: 1.0; source: canon neoclásico (anchura alar = intercantal); Farkas: la mayoría lo supera ligeramente |
| `mouth_width` | Anchura bucal (cheilion a cheilion) |  | px | — |
| `mouth_to_nose` | Ratio boca/nariz |  | ratio | ideal: 1.5; typical: 1.5–1.65; source: canon neoclásico 1.5; Farkas 1985 ≈ 1.6 |
| `philtrum_length` | Longitud del filtrum (subnasale→labiale superius) |  | px | — |
| `lip_ratio` | Ratio labio superior / inferior (altura de vermellón) |  | ratio | ideal: 1:1.6 (0.62); typical: 0.5–0.8; source: Penna et al. 2015; proporción áurea citada en literatura estética |
| `lip_height_to_mouth_width` | Altura total de labios / anchura bucal |  | ratio | — |
| `commissure_tilt` | Tilt de comisuras | ángulo medio de (stomion→cheilion) respecto a la horizontal; + = comisuras hacia arriba | deg | typical: -2 a +4; source: orientativo |
| `lower_face_height` | Altura del tercio inferior (subnasale→menton) |  | px | — |
| `chin_height` | Altura del mentón (sublabiale→menton) |  | px | — |
| `chin_to_lower_face` | Mentón / tercio inferior |  | ratio | ideal: ≈0.5 (sublabiale divide el tercio inferior); source: análisis de Powell & Humphreys / Legan |
| `bigonial_width` | Anchura bigonial (mandíbula) |  | px | — |
| `bizygomatic_width` | Anchura bizigomática |  | px | — |
| `jaw_to_cheek` | Ratio mandíbula / pómulos (bigonial / bizigomático) |  | ratio | typical_male: 0.75–0.85; typical_female: 0.70–0.80; source: Farkas (bigonial ≈ 97–100 mm, bizigomático ≈ 130–140 mm) |
| `chin_width_to_jaw` | Anchura de mentón / bigonial |  | ratio | — |
| `brow_position` | Posición de ceja (apex→pupila / anchura de ojo) |  | ratio | typical: 0.3–0.5 (más alto = ceja más elevada); source: orientativo |
| `brow_tilt` | Inclinación de ceja (cabeza→cola) | + = cola más alta que cabeza | deg | typical: +5 a +15; source: orientativo |
| `midface_ratio` | Ratio de tercio medio (interpupilar / pupila→labiale superius) |  | ratio | ideal: ≈1.0; source: orientativo, usado en estética facial |
| `symmetry` | Simetría bilateral |  | score | note: índice interno 0–100; no comparable con otras herramientas |
| `sagittal_angles` | Ángulos sagitales estimados desde la malla 3D (nasofrontal, nasolabial, mentolabial) |  | deg | nasofrontal: 115–135; nasolabial: 90–110 (M) / 95–115 (F); mentolabial: 120–135; source: Naini 2011; Powell & Humphreys 1984 |

## Normas empíricas

Cada medida se compara con 1638 caras frontales de MEBeauty (6 ascendencias × 2 sexos, 84–338 por grupo) pasadas por el mismo pipeline. Se devuelve percentil, media y z dentro del grupo `sexo|ascendencia`; si no hay sexo o ascendencia declarados se usa `all`.

## Validación de repetibilidad (FEI, 50 sujetos × 3 fotos)

| Grupo | CV % mediano | Criterio |
|---|---|---|
| Longitudes y ratios | 0,3 – 2,9 | < 3 % (39 de 43 cumplen) |
| Altura de ojo, simetría, altura de labios | 3,0 – 4,2 | sensibles a expresión y parpadeo |
| Ángulos (cantal, ceja, nasofrontal, nasolabial) | SD 0,4 – 0,7° | < 1,5° |
| Tilt de comisuras, mentolabial | SD 1,4 – 1,5° | límite |
