#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

echo "Stopping NuclearShield..."
docker compose down --remove-orphans
echo "NuclearShield services stopped."
