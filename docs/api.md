# API HTTP

La API escucha en `http://127.0.0.1:8766` (`FACELAB_PORT` para cambiarlo) y el front Next.js en `http://localhost:3000`, que reenvía `/api/*`, `/out/*`, `/analyze` y `/reports` a la API. Sin autenticación: es una herramienta local. Si lo expones, ponle un proxy con acceso restringido (ver [deploy.md](deploy.md)).

## Páginas (front, `web/`)

| Ruta | Qué es |
|---|---|
| `/` | Portada con onboarding de 5 pasos (`#analizar` lo abre) |
| `/feed` | Feed de personas analizadas (rejilla e historias) |
| `/report/<stem>` | Informe progresivo en modo Simple o Ciencia. `?print=1` fuerza Ciencia y marca `data-ready` para el PDF |
| `/story/<stem>` | Tarjetas 9:16 apiladas. `?card=n` muestra solo una a 1080×1920 |
| `/people`, `/compare?a=&b=` | Línea temporal por persona y comparación de dos informes |
| `/admin`, `/admin/<stem>` | Cola de revisión humana y editor |

Si se pide una de estas rutas al puerto de la API, responde con una redirección al front (`FACELAB_WEB_URL`).

## Análisis

### `POST /analyze` (multipart)

| Campo | Tipo | Notas |
|---|---|---|
| `file` | imagen | Foto frontal (obligatoria) |
| `profile_photo` | imagen | Foto lateral a 90° (opcional) |
| `sex` | `male` \| `female` \| `""` | Grupo de referencia |
| `ancestry` | `asian` \| `black` \| `caucasian` \| `hispanic` \| `indian` \| `mideastern` \| `other` \| `""` | |
| `age` | entero | Edad declarada |
| `person` | texto | Nombre o apodo (feed, tarjetas, seguimiento) |
| `ambition` | `""` \| `mejora` \| `glow-up` | Nivel mínimo del protocolo; nunca rebaja el calculado |
| `feed` | `1` \| `0` | Aparecer en el feed (por defecto sí) |
| `full` | `1` \| `0` | `0` solo calcula landmarks y recortes |

Respuesta: `{"stem": "...", "report_url": "/report/<stem>"}`. El informe se completa en segundo plano.

```bash
curl -F file=@foto.jpg -F sex=male -F ancestry=hispanic -F age=25 -F person=Diego \
     http://localhost:8766/analyze
```

### `GET /api/status/<stem>`

```json
{"steps":[{"id":"analysis","label":"Landmarks y medidas","state":"done","detail":"32 medidas con percentil"}, ...],
 "current":"looks","done":false,"error":null,"updated":1788669046.1}
```

Estados: `pending`, `running`, `done`, `error`, `skipped`. Pasos: `analysis`, `visual`, `style`, `profile`, `narrative`, `protocol`, `visualize`, `looks`.

### `GET /api/report/<stem>`

El JSON completo del informe más `catalog` (nombre, norma y unidad de cada medida), `stem` y `json_path`. Ver [report-json.md](report-json.md) para la estructura.

### `POST /api/regen/<stem>`

```json
{"steps": ["narrative", "protocol", "visualize"], "ambition": "glow-up", "look_ids": ["corte_2"]}
```

- `steps` por defecto: narrativa, protocolo y visualización. Cualquier subconjunto de los ocho pasos.
- `ambition` actualiza el perfil y se guarda.
- `look_ids` limita el paso `looks` a esas tarjetas (ids de `style.advice.outfits`, `haircuts` y `grooming`).

### `PUT /api/review/<stem>`

```json
{"narrative": {...}, "protocol": {...}, "review": {"approved": true, "by": "Ana", "notes": "..."}}
```

Guarda ediciones humanas de narrativa y protocolo y el estado de revisión. El informe muestra el badge "revisado por".

## Salidas

| Ruta | Qué devuelve |
|---|---|
| `GET /api/feed` | Lista pública: `stem`, `name`, `date`, `face`, `global`, `symmetry`, `proportionality`, `averageness`, `visual_age`, `season`, `season_hex`, `face_shape`, `strength`, `headline`, `reviewed`, `after`, `look` |
| `GET /reports` | Lista interna con scores y flags (`has_narrative`, `has_protocol`, `review`) |
| `GET /api/pdf/<stem>` | PDF A4 con portada (Chrome headless, ~9 s) |
| `GET /api/card/<stem>/<n>` | PNG 1080×1920 de la tarjeta `n` (0–5) |
| `GET /out/<archivo>` | Cualquier imagen o archivo de `out/mine` |

## Endpoints síncronos (legado)

`POST /narrate`, `POST /protocol`, `POST /visualize` con `{"json_path": "..."}` ejecutan un paso y esperan. Se mantienen para scripts; la UI usa `/api/regen`.

## Línea de comandos

```bash
uv run python -m facelab analyze foto.jpg -o out/foto.json --debug out/foto_debug.jpg
uv run python -m facelab analyze foto.jpg --sex female --ancestry asian --age 30 --narrate --protocol -o out/foto.json
uv run python -m facelab.repeat samples/fei out/fei_repeat.json        # repetibilidad
uv run python -m facelab.build_norms samples/mebeauty norms/mebeauty_features.jsonl
uv run python -m facelab.build_skin_norms samples/mebeauty norms/mebeauty_skin.jsonl
uv run python -m facelab.attractiveness                                # reentrena el modelo ridge
```
