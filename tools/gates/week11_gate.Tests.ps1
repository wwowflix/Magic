$ErrorActionPreference='Stop'
$PSDefaultParameterValues['*:Encoding']='utf8'
$ROOT = $env:MAGIC_ROOT; if (-not $ROOT) { $ROOT = (Get-Location).Path }
$remMetrics = Join-Path $ROOT 'outputs\remediation\remediate_metrics.json'
$alertLog   = Join-Path $ROOT 'outputs\remediation\alert_log.jsonl'
$cutoff = (Get-Date).AddHours(-48)

function Get-LatestMetric {
  if (-not (Test-Path $remMetrics)) { return $null }
  try { (Get-Content $remMetrics -Raw | ConvertFrom-Json) | Select-Object -Last 1 } catch { $null }
}

Describe 'Week 11 Gate' {
  It '11.1 Remediation metric exists and recent' {
    $m = Get-LatestMetric
    if (-not $m) { $false | Should Be $true }
    else {
      $ts = [datetime]::Parse(($m.ts -replace 'Z$'))
      (($ts -gt $cutoff) -and ((0+$m.attempted) -gt 0)) | Should Be $true
    }
  }
  It '11.4 Alert log exists' {
    (Test-Path $alertLog) | Should Be $true
  }
}
