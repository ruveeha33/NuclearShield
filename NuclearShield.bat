@echo off
setlocal EnableExtensions
cd /d "%~dp0"
cls
echo ================================================================
echo                    N U C L E A R S H I E L D
echo        Advanced Nuclear Facility Cybersecurity Simulation
echo ================================================================
echo.
echo  [1] Full Exam Demo     - Terminal + Grafana + Prometheus
echo  [2] Terminal SOC       - Combined synthetic scenario
echo  [3] SCADA Protection   - OT monitoring scenario
echo  [4] Safety Integrity   - Safety-system assurance scenario
echo  [5] Material Security  - MC&A safeguards scenario
echo  [6] Insider Risk       - Physical-cyber access scenario
echo  [7] Architecture       - Show defense-in-depth concept
echo  [0] Exit
echo.
set /p choice=Select option: 

if "%choice%"=="0" exit /b 0
if not exist .venv py -m venv .venv
call .venv\Scripts\activate
python -m pip install --upgrade pip >nul
pip install -r requirements.txt >nul

if "%choice%"=="1" python -m nuclearshield --monitoring --scenario combined
if "%choice%"=="2" python -m nuclearshield --scenario combined
if "%choice%"=="3" python -m nuclearshield --scenario scada-anomaly
if "%choice%"=="4" python -m nuclearshield --scenario safety-integrity
if "%choice%"=="5" python -m nuclearshield --scenario material-variance
if "%choice%"=="6" python -m nuclearshield --scenario insider-risk
if "%choice%"=="7" python -m nuclearshield --architecture

echo.
pause
