#!/usr/bin/env bash
# Arranca la API (FastAPI, :8766) y el front (Next.js, :3000) a la vez. Ctrl+C para parar los dos.
set -e
cd "$(dirname "$0")"
[ -d web/node_modules ] || (cd web && bun install)
uv run python -m facelab.serve &
API=$!
trap 'kill $API 2>/dev/null' EXIT
cd web && bun run dev
