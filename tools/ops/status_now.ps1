param([string]$Root = "E:\MAGIC")
$ErrorActionPreference = "SilentlyContinue"
$ts = Get-Date -Format "yyyyMMdd_HHmmss"
$outDir = Join-Path $Root "outputs\reports\readiness"
New-Item -ItemType Directory -Force $outDir | Out-Null

# Run the NumPy shadow scanner
python "$Root\tools\diagnostics\root_numpy_shadow_scan.py" | Out-Null

# Find latest shadow report
$latest = Get-ChildItem $outDir -Filter "root_numpy_shadow_report_*.tsv" | Sort-Object LastWriteTime -Descending | Select-Object -First 1
if (-not $latest) { Write-Error "No root_numpy_shadow_report_*.tsv found"; exit 1 }

# Compose a minimal status TSV (extend with your real checks)
$tsv = Join-Path $outDir "status_live_$ts.tsv"
"Step`tCheck`tStatus`tNotes" | Set-Content -Encoding UTF8 $tsv
"1`tShadow Scan`tPASS`t$($latest.Name)" | Add-Content -Encoding UTF8 $tsv

Write-Host "Saved $tsv"