# tools\magic_status_hub_compat.ps1
$ErrorActionPreference = "Stop"

# Move to repo root (this file is expected in tools/)
Set-Location (Split-Path -Parent $PSCommandPath) | Out-Null
Set-Location ..  # go to E:\MAGIC

# Optional: run a scan if you have a Python scanner
if (Test-Path .\tools\magic_full_status_scan.py) {
  try { .\venv\Scripts\python.exe .\tools\magic_full_status_scan.py } catch { Write-Warning $_.Exception.Message }
}

# Read the JSON results
$json = ".\outputs\reports\magic_full_status.json"
if (-not (Test-Path $json)) {
  Write-Warning "No results at $json. Showing fallback listing."
  Get-ChildItem . -Recurse -Include *week*,*phase* | Select-Object FullName | Format-Table -AutoSize
  exit 0
}

try { $rows = Get-Content -Raw $json -Encoding UTF8 | ConvertFrom-Json } catch { Write-Warning $_.Exception.Message; exit 1 }
if (-not $rows) { Write-Warning "Result set is empty."; exit 0 }

# Normalize and display
$view = $rows | ForEach-Object {
  [pscustomobject]@{
    component = $_.component
    metric    = $_.metric
    status    = $_.status
    details   = (($_.details) | Out-String).Trim()
    observed  = $_.observed_at
  }
}

$view | Format-Table -AutoSize

# Save CSV/TSV
$csv = ".\outputs\reports\magic_quick_status.csv"
$tsv = ".\outputs\reports\magic_quick_status.tsv"
$view | Export-Csv $csv -NoTypeInformation -Encoding UTF8
$view | ConvertTo-Csv -NoTypeInformation | % { $_ -replace ',', "`t" } | Set-Content $tsv -Encoding UTF8

Write-Host "`nSaved:" -ForegroundColor Cyan
Write-Host "  $csv"
Write-Host "  $tsv"
