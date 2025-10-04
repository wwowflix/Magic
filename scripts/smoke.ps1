Param()
$logs = (Resolve-Path .\outputs\logs).Path
mkdir $logs -Force | Out-Null
$img = 'wwowdocker/magic:test'

# Container responds to --help and writes a summary via bind mount
docker run --rm $img --help | Out-Null
docker run --rm -v "${logs}:/app/outputs/logs" $img --summary /app/outputs/logs/runner_summary.tsv | Out-Null

if (-not (Test-Path (Join-Path $logs 'runner_summary.tsv'))) {
  throw 'No summary generated'
}
Write-Host '✅ Smoke OK'
