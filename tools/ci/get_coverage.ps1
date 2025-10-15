param([string]$Workflow="tests.yml", [string]$Branch="$(git rev-parse --abbrev-ref HEAD)")
$rid  = gh run list --workflow $Workflow --branch $Branch --limit 1 --json databaseId --jq ".[0].databaseId"
if(-not $rid){ Write-Host "No run found yet." -ForegroundColor Yellow; exit 0 }
$temp = Join-Path $env:TEMP ("cov_" + $rid)
Remove-Item $temp -Recurse -Force -ErrorAction SilentlyContinue; New-Item $temp -ItemType Directory | Out-Null
try{
  gh run download $rid --name coverage-xml --dir $temp | Out-Null
} catch {
  Write-Host "No coverage-xml artifact yet." -ForegroundColor Yellow; exit 0
}
$covPath = Join-Path $temp "coverage.xml"
if(!(Test-Path $covPath)){ Write-Host "coverage.xml missing in artifact." -ForegroundColor Yellow; exit 0 }
[xml]$cov = Get-Content $covPath -Raw
$pct = [math]::Round([double]$cov.coverage."line-rate" * 100, 2)
"Coverage: $pct%"
