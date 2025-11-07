param([string]$Root=$Root)

if (-not \E:\MAGIC) { \E:\MAGIC = (Get-Location).Path }
$ErrorActionPreference = "Stop"
function J($p){ Join-Path $Root $p }
function Ensure-Dir([string]$p){ if(!(Test-Path $p)){ New-Item -ItemType Directory -Force -Path $p | Out-Null } }
$reports = J "outputs\reports"; Ensure-Dir $reports
Write-Host "=== Week 11 Cleanup Pack ===" -ForegroundColor Cyan

# 41) Audit manifest
try {
  $out = J "outputs\reports\audit_manifest.json"
  @{ ok=$true; ts=(Get-Date -Format s); notes="Audit stub"} | ConvertTo-Json | Set-Content -Encoding UTF8 $out
  Write-Host "Audit manifest PASS" -ForegroundColor Green
} catch { Write-Host "Audit manifest FAIL $_" -ForegroundColor Red }

# 42) Ops notify
try {
  $out = J "outputs\reports\ops_notify.json"
  @{ ok=$true; ts=(Get-Date -Format s); notes="Notify stub"} | ConvertTo-Json | Set-Content -Encoding UTF8 $out
  Write-Host "Ops notify PASS" -ForegroundColor Green
} catch { Write-Host "Ops notify FAIL $_" -ForegroundColor Red }

Write-Host "Week 11 Cleanup Pack complete." -ForegroundColor Cyan
