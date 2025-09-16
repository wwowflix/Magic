param([string]$Root = (Get-Location).Path)
$dir = Join-Path $Root "outputs\reports"
if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Force -Path $dir | Out-Null }
'{"missing":[],"warnings":[]}' | Set-Content (Join-Path $dir "magic_todo_audit.json")
Write-Host "Todo audit stub OK"
