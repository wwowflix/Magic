param()
$ErrorActionPreference = 'Stop'
$module = 'H'
$generic = Join-Path (Split-Path $MyInvocation.MyCommand.Path -Parent) 'ci_phase11_guard.ps1'
if (-not (Test-Path $generic)) { Write-Error "Missing $generic"; exit 2 }
powershell -NoProfile -ExecutionPolicy Bypass -File $generic -Module $module
