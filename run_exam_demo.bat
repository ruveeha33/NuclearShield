@echo off
setlocal EnableExtensions
cd /d "%~dp0"
title NuclearShield - Exam Demonstration

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
python -c "import rich, sklearn, prometheus_client, numpy" >nul 2>&1
if errorlevel 1 (
  echo Installing NuclearShield dependencies...
  python -m pip install --upgrade pip >nul
  pip install -r requirements.txt >nul
  if errorlevel 1 (
    echo [ERROR] NuclearShield dependencies could not be installed.
    pause
    exit /b 1
  )
)

python -m nuclearshield --self-check
if errorlevel 1 (
  echo [ERROR] NuclearShield readiness check failed.
  pause
  exit /b 1
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
