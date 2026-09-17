@echo off
setlocal

cd /d "%~dp0"

echo Stopping NuclearShield...
docker compose down --remove-orphans

echo.
echo NuclearShield services stopped.
pause
