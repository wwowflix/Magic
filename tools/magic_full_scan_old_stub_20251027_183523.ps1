param([string]$Root = (Get-Location).Path)
$dir = Join-Path $Root "outputs\reports"
if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Force -Path $dir | Out-Null }
$orph = Join-Path $dir "orphans.tsv"
if (Test-Path ".\tools\magic_full_tree_audit.ps1") {
  powershell -NoProfile -ExecutionPolicy Bypass -File ".\tools\magic_full_tree_audit.ps1" -Root $Root -LargeMB 200 -OldDays 120 -HashMaxMB 1024
} else {
  "path`tSizeBytes`tDir" | Set-Content $orph
}
Write-Host "Full scan stub OK"
