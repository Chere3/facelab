# Instalación y despliegue

## Requisitos

- macOS o Linux con Python 3.11 y [uv](https://docs.astral.sh/uv/). En Apple Silicon todo corre en CPU sin configuración.
- [Bun](https://bun.sh) para el front (Next.js).
- ~3 GB de disco: dependencias (torch, transformers, mediapipe, opencv) y modelos descargados en el primer uso.
- Para narrativa, protocolo y asesoría: [Claude Code](https://claude.com/claude-code) instalado y con sesión iniciada. facelab usa el Agent SDK con esa sesión; no necesita API key.
- Para proyecciones y looks: [Codex CLI](https://github.com/openai/codex) (`codex`) con acceso a `gpt-5.5` e `image_gen`.
- Para PDF y tarjetas PNG: Google Chrome o Chromium.

Sin Claude ni Codex el resto funciona: medidas, percentiles, piel, colorimetría, camisas, perfil y PDF.

## Instalación

```bash
git clone https://github.com/Chere3/facelab && cd facelab
uv sync
./dev.sh                     # API en :8766 + front en :3000 (instala web/ la primera vez)
# → http://localhost:3000
```

Para producción local: `cd web && bun run build && bun run start` sirve el front compilado en :3000; la API sigue con `uv run python -m facelab.serve`.

Variables de entorno:

| Variable | Por defecto | Para qué |
|---|---|---|
| `FACELAB_PORT` | `8766` | Puerto de la API |
| `FACELAB_WEB_URL` | `http://localhost:3000` | URL del front; la usan el PDF y las tarjetas PNG (Chrome headless) y las redirecciones |
| `FACELAB_API` (en `web/`) | `http://127.0.0.1:8766` | URL de la API a la que el front hace proxy |
| `FACELAB_LOOK_PARALLEL` | `3` | Renders de Codex simultáneos |
| `HF_TOKEN` | — | Descargas más rápidas de Hugging Face |

## Estructura de datos

```
samples/mine/   fotos subidas (<stem>.jpg, <stem>_profile.jpg)
out/mine/       <stem>.json · <stem>.meta.json · <stem>.status.json · imágenes · PDF
norms/          features derivadas de MEBeauty y modelo de atractivo
models/         modelos descargados (.task)
```

`samples/` y `out/` están en `.gitignore`. Contienen caras: no los subas a ningún sitio.

## Compartir con otras personas

facelab no tiene autenticación. Tres opciones, de más a menos segura:

1. **Tailscale Serve** (solo tu tailnet): `tailscale serve --bg 3000` (el front hace proxy a la API). Solo tus dispositivos y los de quien invites.
2. **Tailscale Funnel** (público con HTTPS): `tailscale funnel --bg 3000`. Cualquiera con el enlace puede subir fotos, lanzar análisis que consumen tu cuenta de Claude y Codex, y entrar en `/admin`. Apágalo con `tailscale funnel --https=443 off`.
3. **Proxy con autenticación** (Caddy, nginx, Cloudflare Access) delante del puerto 3000, restringiendo al menos `/analyze`, `/api/regen` y `/admin`.

## Actualizar normas

Las normas empíricas viven en `norms/mebeauty_features.jsonl` (1638 caras) y `norms/mebeauty_skin.jsonl`. Para reconstruirlas necesitas el dataset MEBeauty en `samples/mebeauty`:

```bash
uv run python -m facelab.build_norms samples/mebeauty norms/mebeauty_features.jsonl
uv run python -m facelab.build_skin_norms samples/mebeauty norms/mebeauty_skin.jsonl
uv run python -m facelab.attractiveness    # reentrena el modelo ridge con las features nuevas
```

## Problemas frecuentes

- **"Perfil lateral" tarda minutos o falla**: fotos de móvil de 4000 px; `profile_view.py` ya reescala a 1200 px. Si sigue fallando, la silueta no se detecta (fondo del mismo tono que la piel).
- **Protocolo en error "respuesta inválida"**: Claude devolvió texto fuera del JSON. Pulsa "Protocolo + imagen" para reintentar; se conserva el anterior.
- **Visualización o looks en error**: `codex` no está en el PATH del proceso, o el modelo no generó el archivo. El mensaje incluye la cola de la salida de Codex.
- **PDF de 60 MB**: los renders eran PNG. Desde la fase 7 se usan JPEG de 720 px; los informes antiguos se convierten al regenerar los looks.
- **La página se queda colgada tras reiniciar el servidor**: recarga la pestaña; el polling quedó en un estado intermedio.
