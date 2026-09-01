@echo off
setlocal EnableExtensions
cd /d "%~dp0"
cls
echo ========================================================================
echo                          N U C L E A R S H I E L D
echo                     FACILITY PROTECTION COMMAND
echo            Safe Defensive Nuclear Cybersecurity Simulation
echo ========================================================================
echo.
echo  [1] EXAM COMMAND MODE    Terminal + Grafana + Prometheus + evidence report
echo  [2] TERMINAL COMMAND     Combined scenario + end-of-session report
echo  [3] SCADA WATCH          OT/SCADA anomaly demonstration
echo  [4] SAFETY WATCH         Safety-I&C integrity demonstration
echo  [5] SAFEGUARDS WATCH     MC&A / material security demonstration
echo  [6] ACCESS WATCH         Insider / physical-cyber demonstration
echo  [7] ARCHITECTURE         Explain defense-in-depth design
echo  [8] SYSTEM SELF-CHECK    Verify local demo prerequisites
echo  [9] ASSURANCE GATES      DevSecOps / configuration-control evidence model
echo  [10] THREAT CONTEXT      Safe nuclear-sector defensive threat context
echo  [0] EXIT
echo.
set /p choice=Command selection: 

if "%choice%"=="0" exit /b 0
if not exist .venv py -m venv .venv
call .venv\Scripts\activate
python -m pip install --upgrade pip >nul
pip install -r requirements.txt >nul

if "%choice%"=="1" python -m nuclearshield --briefing --monitoring --scenario combined --report --export-report
if "%choice%"=="2" python -m nuclearshield --briefing --scenario combined --report
if "%choice%"=="3" python -m nuclearshield --briefing --scenario scada-anomaly --report
if "%choice%"=="4" python -m nuclearshield --briefing --scenario safety-integrity --report
if "%choice%"=="5" python -m nuclearshield --briefing --scenario material-variance --report
if "%choice%"=="6" python -m nuclearshield --briefing --scenario insider-risk --report
if "%choice%"=="7" python -m nuclearshield --architecture
if "%choice%"=="8" python -m nuclearshield --self-check
if "%choice%"=="9" python -m nuclearshield --assurance
if "%choice%"=="10" python -m nuclearshield --threat-context

echo.
echo Session finished. No real OT or nuclear control actions were performed.
pause
