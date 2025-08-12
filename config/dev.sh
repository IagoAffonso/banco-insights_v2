#!/usr/bin/env bash

set -euo pipefail

# Change to repo root
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
cd "$ROOT_DIR"

# Load root .env if present
if [ -f .env ]; then
  # shellcheck disable=SC1091
  source .env
fi

# Defaults
PORT="${PORT:-8001}"
NEXT_PUBLIC_API_BASE_URL="${NEXT_PUBLIC_API_BASE_URL:-http://127.0.0.1:${PORT}}"
CORS_ORIGINS="${CORS_ORIGINS:-http://localhost:3000,http://localhost:3001}"

echo "==> Starting Banco Insights dev environment"
echo "    Backend port: ${PORT}"
echo "    Frontend: http://localhost:3000"
echo "    NEXT_PUBLIC_API_BASE_URL: ${NEXT_PUBLIC_API_BASE_URL}"
echo "    CORS_ORIGINS: ${CORS_ORIGINS}"

# Helper to check command
has_cmd() { command -v "$1" >/dev/null 2>&1; }

BACKEND_PID=""
FRONTEND_PID=""

cleanup() {
  echo "\n==> Shutting down..."
  if [ -n "$FRONTEND_PID" ] && kill -0 "$FRONTEND_PID" 2>/dev/null; then
    kill "$FRONTEND_PID" || true
  fi
  if [ -n "$BACKEND_PID" ] && kill -0 "$BACKEND_PID" 2>/dev/null; then
    kill "$BACKEND_PID" || true
  fi
  wait || true
}

trap cleanup INT TERM EXIT

# Start backend (FastAPI via uvicorn)
(
  cd backend
  echo "==> [backend] Starting uvicorn on :${PORT}"
  # Prefer uvicorn if available, else python -m uvicorn
  if has_cmd uvicorn; then
    PORT="$PORT" CORS_ORIGINS="$CORS_ORIGINS" uvicorn main:app --reload --host 0.0.0.0 --port "$PORT"
  else
    echo "[backend] 'uvicorn' not found on PATH. Attempting 'python -m uvicorn'."
    PORT="$PORT" CORS_ORIGINS="$CORS_ORIGINS" python -m uvicorn main:app --reload --host 0.0.0.0 --port "$PORT"
  fi
) & BACKEND_PID=$!

# Start frontend (Next.js)
(
  cd frontend
  echo "==> [frontend] Starting Next.js dev server"
  NEXT_PUBLIC_API_BASE_URL="$NEXT_PUBLIC_API_BASE_URL" npm run dev
) & FRONTEND_PID=$!

echo "==> Both services started (PIDs: backend=$BACKEND_PID, frontend=$FRONTEND_PID)"
echo "    Open http://localhost:3000 in your browser."

# Wait for any to exit
wait -n || true

# Trigger cleanup (trap will handle)
exit 0

