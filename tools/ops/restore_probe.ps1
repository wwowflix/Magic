param([string]$Root="D:\MAGIC")
$dst = Join-Path $Root "outputs\restore_probe"
New-Item -ItemType Directory -Force -Path $dst | Out-Null
$rclone = (Get-Command rclone).Source
& $rclone copy "remote:MAGIC/outputs/reports" $dst --update --log-file (Join-Path $Root "outputs\logs\rclone_restore.log") --log-level INFO
"restore drill ok $(Get-Date -Format s)" | Set-Content -Encoding UTF8 (Join-Path $Root "outputs\reports\restore_probe_receipt.txt")
