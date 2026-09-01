@echo off
setlocal EnableExtensions
cd /d "%~dp0"
echo.
echo NuclearShield - stopping local monitoring services...
where docker >nul 2>&1
if errorlevel 1 (
  echo Docker was not found. Nothing to stop.
  exit /b 0
)
docker compose -f docker-compose.yml down
echo NuclearShield Grafana and Prometheus services stopped.
