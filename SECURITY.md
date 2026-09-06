# Seguridad y privacidad

facelab procesa fotos de caras en el ordenador donde corre. Estas son las garantías y los límites.

## Qué sale del ordenador

- El texto de la narrativa, el protocolo y la asesoría de estilo se envía a Claude (Agent SDK, sesión de Claude Code).
- La foto de busto se envía a Codex (`codex exec` con `image_gen`) para las proyecciones y los looks.
- Los modelos (MediaPipe, SegFormer, InsightFace, face-alignment) se descargan una vez y corren en local.

Nada más sale. No hay telemetría.

## Si expones el servidor

`facelab.serve` escucha en `127.0.0.1:8766` y no tiene autenticación. Si lo publicas (Tailscale Funnel, ngrok, un proxy), cualquiera con el enlace puede subir fotos, lanzar análisis que consumen tu cuenta de Claude y Codex, ver todos los informes y usar la cola de revisión. Ponle un proxy con autenticación o una allowlist antes.

## Reportar una vulnerabilidad

Abre un issue con la etiqueta `security` o escribe a los mantenedores. Describe el problema y cómo reproducirlo; no incluyas fotos de terceros.
