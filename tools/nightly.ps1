param()
$ErrorActionPreference = "Stop"

# --- Paths ---
$Root   = "D:\MAGIC"
$Py     = Join-Path $Root "venv\Scripts\python.exe"
$Helper = Join-Path $Root "tmp\compile_ready_helper.py"

# --- Compile check (suppress Python warnings) ---
$env:PYTHONWARNINGS = "ignore"
$json = & $Py -W ignore $Helper 2>$null
$rep  = $json | ConvertFrom-Json
"[nightly] remaining_fails: {0}" -f $rep.failed | Write-Host

# --- Update compile_summary.tsv (tab-delimited) ---
$Reports = Join-Path $Root "outputs\reports"
$Backups = Join-Path $Root "outputs\backups"
New-Item -ItemType Directory -Force -Path $Reports | Out-Null

$today = (Get-Date).Date

$indentfix_dirs = Get-ChildItem $Backups -Directory -Filter "indentfix_*" |
                  Where-Object { $_.LastWriteTime.Date -eq $today }
$healed = (
  $indentfix_dirs | ForEach-Object {
    Get-ChildItem -Recurse $_.FullName -File -Include *.py
  } | Measure-Object
).Count

$quarantine_root = Join-Path $Root "quarantine\compile_fail"
$quarantined = if(Test-Path $quarantine_root){
  (Get-ChildItem -Recurse $quarantine_root -File | Where-Object { $_.LastWriteTime.Date -eq $today }).Count
} else { 0 }

$stubbed = (
  Get-ChildItem $Backups -Directory -Filter "stubs_*" |
  Where-Object { $_.LastWriteTime.Date -eq $today } |
  ForEach-Object { Get-ChildItem -Recurse $_.FullName -File } |
  Measure-Object
).Count

$tsv = Join-Path $Reports "compile_summary.tsv"
@"
metricvalue
remaining_fails$($rep.failed)
healed_in_indentfix$healed
quarantined_today$quarantined
stubbed_today$stubbed
"@ | Set-Content -LiteralPath $tsv -Encoding UTF8
"[nightly] updated: $tsv" | Write-Host

# --- Module F (Error Pattern Analyzer) ---
& $Py "D:\MAGIC\scripts\phase11\module_F\11F_error_pattern_analyzer_READY.py" 2>$null | Write-Host

# --- Module D (Deps / Orphan Audit) ---
& $Py "D:\MAGIC\scripts\phase11\module_D\11D_dependency_orphan_audit_READY.py" 2>$null | Write-Host

exit 0
