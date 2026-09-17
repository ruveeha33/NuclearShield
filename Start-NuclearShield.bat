@echo off
setlocal

cd /d "%~dp0"

echo.
echo ============================================
echo  NuclearShield - Defensive Assurance Console
echo ============================================
echo.

where docker >nul 2>&1
if errorlevel 1 (
    echo ERROR: Docker was not found.
    echo Install Docker Desktop first:
    echo https://www.docker.com/products/docker-desktop/
    pause
    exit /b 1
)

docker info >nul 2>&1
if errorlevel 1 (
    echo ERROR: Docker Desktop is installed but not running.
    echo Start Docker Desktop and try again.
    pause
    exit /b 1
)

powershell -ExecutionPolicy Bypass -File "%~dp0start-nuclearshield.ps1"

if errorlevel 1 (
    echo.
    echo NuclearShield did not start successfully.
    pause
    exit /b 1
)

exit /b 0
