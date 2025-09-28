param([string]$Root="D:\MAGIC")
$ErrorActionPreference = "Stop"
function J([string]$p){ Join-Path $Root $p }
$logs = J "outputs\logs"; if(!(Test-Path $logs)){ New-Item -ItemType Directory -Force -Path $logs | Out-Null }

# full path to rclone (helps in scheduled tasks)
$rclone = (Get-Command rclone).Source

# avoid re-uploads just to set modtime on Dropbox
& $rclone copy (J "outputs") "remote:MAGIC/outputs" --update --use-server-modtime `
  --log-file (J "outputs\logs\rclone_backup.log") --log-level INFO

"offsite backup complete (Dropbox via rclone) $(Get-Date -Format s)" |
  Set-Content -Encoding UTF8 (J "outputs\reports\offsite_backup_receipt.txt")
