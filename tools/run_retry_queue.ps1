$ErrorActionPreference = "Stop"
python tools/extract_retry_queue.py
if (Test-Path retry_queue.json) {
  $queue = Get-Content retry_queue.json -Raw | ConvertFrom-Json
  if ($null -ne $queue -and $queue.Count -gt 0) {
    $names = ($queue | ForEach-Object { $_.script }) -join ","
    Write-Host "Re-running failed scripts: $names"
    # Ensure your runner supports --only-scripts "<comma list>"
    python self_healing_runner_v5.py --only-scripts "$names"
  } else {
    Write-Host "No failed scripts to retry."
  }
} else {
  Write-Host "No retry_queue.json found."
}
