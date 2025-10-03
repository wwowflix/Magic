param(
  [string]$Image = "wwowdocker/magic:latest",
  [string]$Out = "D:\MAGIC\outputs\logs\runner_summary.tsv"
)

Write-Host " Pulling $Image..."
docker pull $Image | Out-Null

$container = "magic-smoke-" + (Get-Random)
Write-Host " Running container: $container"
docker run --rm -d --name $container `
  -v "D:\MAGIC\outputs:/app/outputs" `
  $Image sleep 120 | Out-Null

Start-Sleep -Seconds 6
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Image}}"

Write-Host " Executing runner inside container..."
docker exec $container python /app/scripts/phase11/self_healing_runner_v5.py --summary /app/outputs/logs/runner_summary.tsv

Write-Host " Tail logs"
docker logs $container --tail 50

Write-Host " Checking summary on host"
if (Test-Path $Out) {
  Get-Content $Out
  docker stop $container | Out-Null
  Write-Host " Smoke OK" -ForegroundColor Green
  exit 0
} else {
  docker stop $container | Out-Null
  Write-Host " Smoke failed: $Out not found" -ForegroundColor Red
  exit 1
}
