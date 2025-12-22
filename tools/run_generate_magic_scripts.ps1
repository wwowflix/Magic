# MAGIC – Convenience runner for generate_magic_scripts.py

$ErrorActionPreference = "Stop"

# 1) Go to project root
$root = Resolve-Path "E:\MAGIC"
Set-Location -LiteralPath $root

# 2) Activate venv if it exists
$venvActivate = Join-Path $root "venv\Scripts\Activate.ps1"
if (Test-Path $venvActivate) {
    . $venvActivate
}

# 3) Run generator
$scriptPath = Join-Path $root "tools\generate_magic_scripts.py"
if (-not (Test-Path $scriptPath)) {
    throw "Cannot find $scriptPath"
}

Write-Host ">>> Running MAGIC auto-script generator..." -ForegroundColor Cyan
python $scriptPath
Write-Host ">>> Done. Check outputs/logs/magic_generate_magic_scripts.log for details." -ForegroundColor Green
