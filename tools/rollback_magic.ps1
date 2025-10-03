param(
  [Parameter(Mandatory=$true)][string]$ToTag
)
Write-Host " Rolling back to wwowdocker/magic:$ToTag"
docker pull "wwowdocker/magic:$ToTag"
docker rm -f magic-live 2>$null | Out-Null
docker run -d --name magic-live wwowdocker/magic:$ToTag
Start-Sleep -Seconds 6
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Image}}"
docker logs magic-live --tail 30
