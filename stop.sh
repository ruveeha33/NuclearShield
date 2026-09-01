#!/usr/bin/env sh
set -eu
cd "$(dirname "$0")"
if ! command -v docker >/dev/null 2>&1; then
  echo "Docker was not found. Nothing to stop."
  exit 0
fi
docker compose -f docker-compose.yml down
echo "NuclearShield Grafana and Prometheus services stopped."
