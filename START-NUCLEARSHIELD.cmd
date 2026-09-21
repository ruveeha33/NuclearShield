@echo off
setlocal EnableExtensions
cd /d "%~dp0"
title NuclearShield Launcher
cls
echo ============================================================
echo  NuclearShield v1.0.8 Enhanced Launcher
echo ============================================================
echo.
if not exist "%~dp0start-nuclearshield.ps1" (
  echo STARTUP BLOCKED: Project files are not together.
  echo.
  echo Windows is running this launcher from a temporary ZIP folder:
  echo   %~dp0
  echo.
  echo If you opened this file inside the ZIP, close this window and either:
  echo   1. Run START-NUCLEARSHIELD-ONE-CLICK.cmd directly from the ZIP, OR
  echo   2. Right-click the ZIP ^> Extract All, then run START-NUCLEARSHIELD.cmd.
  echo.
  echo The normal launcher intentionally will not continue with missing project files.
  echo ============================================================
  pause
  exit /b 2
)
if not exist "%~dp0docker-compose.yml" (
  echo STARTUP BLOCKED: docker-compose.yml is missing from this folder.
  echo Extract the complete project before using the normal launcher.
  pause
  exit /b 2
)
echo This window will stay open so startup errors are visible.
echo.
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0start-nuclearshield.ps1"
set "EXITCODE=%ERRORLEVEL%"
echo.
if not "%EXITCODE%"=="0" (
  echo ============================================================
  echo  NuclearShield could not start. Exit code: %EXITCODE%
  echo  Review the message above and launcher-diagnostics.log.
  echo ============================================================
) else (
  echo ============================================================
  echo  NuclearShield startup completed successfully.
  echo  Docker services continue running after this window closes.
  echo ============================================================
)
echo.
pause
exit /b %EXITCODE%
