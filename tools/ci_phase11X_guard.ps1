$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent (Split-Path -Parent $PSCommandPath)
$sum  = Join-Path $root 'outputs\logs\master_orchestrator_summary.tsv'
if (!(Test-Path $sum)) { throw "Missing orchestrator summary: $sum" }
$rows = Get-Content -LiteralPath $sum | Where-Object { $_ -match 'scripts\\phase11\\module_X\\' }
if (-not $rows) { throw "No rows for module_X in orchestrator summary." }
$bad = $rows | Where-Object { $_ -match "	ERROR$" -or $_ -match "	FAIL$" }
if ($bad) {
  Write-Host "Phase11X errors found:" -ForegroundColor Red
  $bad | ForEach-Object { Write-Host "  $_" -ForegroundColor Red }
  exit 1
} else {
  Write-Host "Phase11X OK [PASS]" -ForegroundColor Green
}
