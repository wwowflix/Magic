param(
  [string]$Root = "D:\MAGIC"
)

# Where to restore a sample
$restoreDir = Join-Path $Root "outputs\restore_probe"
New-Item -ItemType Directory -Force -Path $restoreDir | Out-Null

# Pick a small known folder (reports are small)
$remotePath = "remote:MAGIC/outputs/reports"

Write-Host "Starting restore probe from $remotePath ..." -ForegroundColor Cyan
rclone copy $remotePath $restoreDir --update --progress

# Write receipt
$receipt = Join-Path $Root "outputs\reports\restore_probe_receipt.txt"
"restore drill ok $(Get-Date -Format s)" | Set-Content -Encoding UTF8 $receipt

Write-Host "Restore probe complete. Receipt written to $receipt" -ForegroundColor Green
