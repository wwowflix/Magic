param([int]$Days=14)
$cut = (Get-Date).AddDays(-$Days)
Get-ChildItem .\outputs\logs -Recurse -File -ErrorAction SilentlyContinue |
  Where-Object { $_.LastWriteTime -lt $cut } | Remove-Item -Force
