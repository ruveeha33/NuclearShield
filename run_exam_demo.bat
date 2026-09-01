@echo off
setlocal EnableExtensions
cd /d "%~dp0"
cls
echo ========================================================================
echo               NUCLEARSHIELD - ONE-CLICK EXAM DEMONSTRATION
echo ========================================================================
echo  Preparing isolated Python environment and defensive monitoring stack...
echo.
if not exist .venv py -m venv .venv
if errorlevel 1 (
  echo [ERROR] Python 3.10+ was not found. Install Python and retry.
  pause
  exit /b 1
)
call .venv\Scripts\activate
python -m pip install --upgrade pip >nul
pip install -r requirements.txt >nul
if errorlevel 1 (
  echo [ERROR] Python dependencies could not be installed.
  pause
  exit /b 1
)
python -m nuclearshield --self-check
if errorlevel 1 (
  echo [ERROR] NuclearShield readiness check failed.
  pause
  exit /b 1
)
cls
python -m nuclearshield --briefing --monitoring --scenario combined --refresh-rate 4 --report --export-report

echo.
echo ========================================================================
echo  DEMO COMPLETE - synthetic evidence is available in the reports folder.
echo  Run stop.bat when you are finished with Grafana/Prometheus.
echo ========================================================================
pause
