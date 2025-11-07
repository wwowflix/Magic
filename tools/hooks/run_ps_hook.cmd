@echo off
REM Usage: run_ps_hook.cmd <script.ps1> [args...]
set "PS1=%~1"
if not exist "%PS1%" (
  echo Hook script not found: %PS1%
  exit /b 1
)
REM Prefer pwsh (PS7), fallback to Windows PowerShell
where pwsh >nul 2>nul
if %ERRORLEVEL%==0 (
  pwsh -NoProfile -ExecutionPolicy Bypass -File "%PS1%" %*
  exit /b %ERRORLEVEL%
) else (
  powershell -NoProfile -ExecutionPolicy Bypass -File "%PS1%" %*
  exit /b %ERRORLEVEL%
)
