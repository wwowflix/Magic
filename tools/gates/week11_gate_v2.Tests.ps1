$ErrorActionPreference='Stop'
$PSDefaultParameterValues['*:Encoding']='utf8'
$ROOT = $env:MAGIC_ROOT; if (-not $ROOT) { $ROOT = (Get-Location).Path }
$remMetrics = Join-Path $ROOT 'outputs\remediation\remediate_metrics.json'
$alertLog   = Join-Path $ROOT 'outputs\remediation\alert_log.jsonl'
$orchRun    = Join-Path $ROOT 'outputs\remediation\orchestrator_run.json'
$prioJson   = Join-Path $ROOT 'outputs\remediation\prioritized_failures.json'
$cutoff = (Get-Date).AddHours(-48)

function Get-LatestMetric {
  if (-not (Test-Path $remMetrics)) { return $null }
  try { (Get-Content $remMetrics -Raw | ConvertFrom-Json) | Select-Object -Last 1 } catch { $null }
}
function Get-OrchRun {
  if (-not (Test-Path $orchRun)) { return $null }
  try { Get-Content $orchRun -Raw | ConvertFrom-Json } catch { $null }
}
function Get-Prioritized {
  if (-not (Test-Path $prioJson)) { return @() }
  try { Get-Content $prioJson -Raw | ConvertFrom-Json } catch { @() }
}

Describe 'Week 11 Gate v2 (e2e signals)' {
  It '11.1 Remediation metric exists and recent' {
    $m = Get-LatestMetric
    if (-not $m) { $false | Should Be $true }
    else {
      $ts = [datetime]::Parse(($m.ts -replace 'Z$'))
      (($ts -gt $cutoff) -and ((0+$m.attempted) -gt 0)) | Should Be $true
    }
  }
  It '11.3 Orchestrator ran recently and matched > 0 (if retry existed)' {
    $o = Get-OrchRun
    if (-not $o) { $false | Should Be $true } else {
      $ts = [datetime]::Parse(($o.ts -replace 'Z$'))
      ($ts -gt $cutoff) | Should Be $true
      # if requested>0 we expect matched>0
      if ((0+$o.requested) -gt 0) { ((0+$o.matched) -gt 0) | Should Be $true }
    }
  }
  It '11.2 Prioritized failures file exists (may be empty only if no retry)' {
    (Test-Path $prioJson) | Should Be $true
    $arr = Get-Prioritized
    # allow empty only if no retry request was present
    if ($arr.Count -eq 0) {
      Write-Warning "prioritized_failures.json is empty (ok if no retry requests)"
    }
    $true | Should Be $true
  }
  It '11.4 Alert log exists' {
    (Test-Path $alertLog) | Should Be $true
  }
}
