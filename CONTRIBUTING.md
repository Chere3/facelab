# Contribuir a facelab

Gracias por querer ayudar. facelab crece sobre todo en tres frentes: **medidas y normas**, **métodos del protocolo** y **producto**. Aquí va cómo trabajar sin romper nada.

## Antes de empezar

- Lee el [Código de conducta](CODE_OF_CONDUCT.md). Resumen: nada de fotos de terceros, nada de juicios de atractivo, fuentes para todo.
- Abre un issue antes de un cambio grande. Para una medida o un método nuevo, cita el paper o el manual en el issue.

## Entorno

```bash
git clone https://github.com/Chere3/facelab && cd facelab
uv sync                      # Python 3.11, todas las dependencias, ~2 GB con torch
uv run pytest -q             # tests ligeros, no descargan modelos
uv run ruff check facelab    # lint
uv run python -m facelab.serve   # http://localhost:8766
```

La primera ejecución descarga MediaPipe FaceLandmarker, SegFormer face-parsing, InsightFace buffalo_l y los pesos de face-alignment. Después todo corre en local.

## Dónde vive cada cosa

| Quiero… | Toco |
|---|---|
| Añadir una medida | `facelab/catalog.yaml` (id, nombre, fórmula, unidad, norma con fuente) y `facelab/measures.py` |
| Añadir un punto antropométrico | `facelab/points.py` (índice de la malla MediaPipe) |
| Añadir un método al protocolo | `facelab/methods.yaml` (id, nombre, `addresses`, evidencia A–D, coste, frecuencia, horizonte, dificultad, tier) |
| Cambiar la colorimetría | `facelab/style.yaml` (estaciones, formas de cara, expresión) y `facelab/colorimetry.py` |
| Cambiar la narrativa o el protocolo de Claude | `facelab/narrate.py`, `facelab/protocol.py`, `facelab/style.py` (prompts de sistema) |
| Cambiar la UI | `facelab/ui.py` (tokens), `landing_page.py`, `feed_page.py`, `report_page.py`, `admin_page.py` |
| Reconstruir normas | `uv run python -m facelab.build_norms samples/mebeauty norms/mebeauty_features.jsonl` |

## Reglas de una medida nueva

1. Fórmula explícita en el catálogo, con los puntos que usa.
2. Unidad: `ratio`, `deg`, `index`, `fraction` o `px`. Lo que está en píxeles no se compara entre personas.
3. Norma citada (autor, año) o `none`. Si es orientativa (por ejemplo, depende de la z de MediaPipe), `caveat` obligatorio.
4. Si quieres percentiles, reconstruye las normas y sube el `.jsonl` actualizado.
5. Test de repetibilidad: `uv run python -m facelab.repeat samples/fei out/fei_repeat.json` debe dar CV < 3 % o SD < 1,5° en la medida nueva.

## Reglas de un método nuevo

- Solo no quirúrgico. Botox y relleno existen como tier `professional` y el protocolo solo los propone con percentil extremo y médico.
- `evidence` honesto: A (ensayos), B (estudios observacionales), C (principio óptico o consenso), D (anecdótico).
- `addresses` lista ids de medidas o conceptos que el método mueve; el protocolo usa esa lista para justificar.

## Pull requests

- Rama desde `main`, un tema por PR.
- `uv run ruff check facelab tests` y `uv run pytest -q` en verde.
- No subas fotos, ni `out/`, ni `samples/`. El `.gitignore` los excluye; no lo cambies.
- Si cambias comportamiento visible, actualiza el README o `docs/`.
- Los mensajes de commit siguen [Conventional Commits](https://www.conventionalcommits.org/): `feat:`, `fix:`, `docs:`, `refactor:`.

## Datos

- **FEI Face Database** (`samples/fei`): uso académico, no se redistribuye. Se usa solo para el test de repetibilidad.
- **MEBeauty** (`samples/mebeauty`): licencia de investigación. En el repo solo viven las *features* derivadas (`norms/*.jsonl`), no las fotos.
- Nunca añadas fotos de personas reales al repositorio, ni siquiera en issues.
