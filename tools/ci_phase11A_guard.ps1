$ErrorActionPreference = 'Stop'
# tools\ci_phase11A_guard.ps1 -> tools (parent) -> repo root (parent)
$root = Split-Path -Parent (Split-Path -Parent $PSCommandPath)
$sum  = Join-Path $root 'outputs\logs\master_orchestrator_summary.tsv'
if (!(Test-Path $sum)) { throw "Missing orchestrator summary: $sum" }

# Look for module_A rows only
$rows = Get-Content -LiteralPath $sum | Where-Object { $_ -match 'scripts\\phase11\\module_A\\' }
if (-not $rows) { throw "No rows for module_A in orchestrator summary." }

# Any trailing status of ERROR or FAIL at the end of the TSV line
$bad = $rows | Where-Object { $_ -match "	ERROR$" -or $_ -match "	FAIL$" }

if ($bad) {
  Write-Host "Phase11A errors found:" -ForegroundColor Red
  $bad | ForEach-Object { Write-Host ("  {0}" -f $_) -ForegroundColor Red }
  exit 1
} else {
  Write-Host "Phase11A OK [PASS]" -ForegroundColor Green
}
