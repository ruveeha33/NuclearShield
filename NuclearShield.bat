@echo off
setlocal EnableExtensions
cd /d "%~dp0"
title NuclearShield - Nuclear Cybersecurity Workstation

if not exist .venv (
  echo Preparing NuclearShield workstation for first use...
  py -m venv .venv
  if errorlevel 1 (
    echo [ERROR] Python 3.10+ was not found. Install Python and retry.
    pause
    exit /b 1
  )
)

call .venv\Scripts\activate
if errorlevel 1 (
  echo [ERROR] Could not activate the NuclearShield virtual environment.
  pause
  exit /b 1
)

python -c "import nuclearshield, rich, sklearn, prometheus_client, numpy" >nul 2>&1
if errorlevel 1 (
  echo Installing NuclearShield and required dependencies...
  python -m pip install --upgrade pip >nul
  python -m pip install -e . >nul
  if errorlevel 1 (
    echo [ERROR] NuclearShield could not be installed into the virtual environment.
    pause
    exit /b 1
  )
)

cls
python -m nuclearshield.launcher
if errorlevel 1 (
  echo.
  echo [ERROR] NuclearShield workstation exited unexpectedly.
  pause
  exit /b 1
)

endlocal
