#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

echo
echo "============================================"
echo " NuclearShield - Defensive Assurance Console"
echo "============================================"
echo

if ! command -v docker >/dev/null 2>&1; then
  echo "ERROR: Docker was not found."
  echo "Install Docker Desktop or Docker Engine first."
  exit 1
fi

if ! docker info >/dev/null 2>&1; then
  echo "ERROR: Docker is installed but the Docker Engine is not running."
  exit 1
fi

if [ ! -f ".env" ]; then
  cp ".env.example" ".env"
  echo "Created .env from .env.example."
fi

docker compose down --remove-orphans

docker compose up --build --pull missing --force-recreate -d

APP_PORT="$(grep '^APP_PORT=' .env | cut -d'=' -f2)"
APP_PORT="${APP_PORT:-8000}"

echo "Waiting for NuclearShield..."

for i in {1..30}; do
  if curl -fsS "http://localhost:${APP_PORT}/api/health" >/dev/null 2>&1; then
    echo "NuclearShield is ready."
    break
  fi
  sleep 2
done

URL="http://localhost:${APP_PORT}"

if command -v open >/dev/null 2>&1; then
  open "$URL"
elif command -v xdg-open >/dev/null 2>&1; then
  xdg-open "$URL"
fi

echo
echo "NuclearShield: $URL"
echo "Prometheus: http://localhost:9090"
echo "Grafana: http://localhost:3000"

