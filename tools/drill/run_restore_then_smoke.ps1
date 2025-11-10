param()
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
Set-Location E:\MAGIC
$logDir = "outputs\logs\week6"; New-Item -ItemType Directory -Force -Path $logDir | Out-Null
$tsv = Join-Path $logDir "restore_status.tsv"
$rows = @()

function Row($k,$v){ [PSCustomObject]@{ Key=$k; Value=$v } }

try {
  python tools\drill\restore_from_latest.py
  $restore = "✅ PASS"
} catch {
  $restore = "⛔ FAIL: $($_.Exception.Message)"
}
$rows += Row "6.4.2 Restore" $restore

try {
  pytest -q
  $smoke = "✅ PASS"
} catch {
  $smoke = "⛔ FAIL"
}
$rows += Row "6.4.3 Post-restore smokes" $smoke

$rows | ForEach-Object { "{0}`t{1}" -f $_.Key, $_.Value } | Set-Content -Path $tsv -Encoding UTF8
Write-Host "Restore drill status TSV: $tsv"
