$ErrorActionPreference = "Stop"
Set-Location (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location ..   # repo root

# Ensure tools on PATH
$env:PYTHONPATH = (Get-Location)

# Run tests
pytest -q | Tee-Object -Variable out
if ($LASTEXITCODE -ne 0) {
  Write-Host "Repo health FAILED" -ForegroundColor Red
  $out | Select-Object -First 200 | ForEach-Object { $_ }
  exit 1
}
Write-Host "Repo health OK" -ForegroundColor Green
