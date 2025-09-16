param([string]$Root = (Get-Location).Path)
$dir = Join-Path $Root "outputs\reports"
if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Force -Path $dir | Out-Null }
"Age>120d`tLarge>200MB`tAction" | Set-Content (Join-Path $dir "cleanup_plan.tsv")
Write-Host "Cleanup plan stub OK"
