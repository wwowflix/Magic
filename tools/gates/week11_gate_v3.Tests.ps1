$ErrorActionPreference='Stop'
$PSDefaultParameterValues['*:Encoding']='utf8'
$ROOT = $env:MAGIC_ROOT; if (-not $ROOT) { $ROOT = (Get-Location).Path }
$remMetrics = Join-Path $ROOT 'outputs\remediation\remediate_metrics.json'
$sugDir     = Join-Path $ROOT 'outputs\remediation\ai_suggestions'
$patchDir   = Join-Path $ROOT 'outputs\remediation\patches'
$cutoff = (Get-Date).AddHours(-48)

function Get-LatestMetric {
  if (-not (Test-Path $remMetrics)) { return $null }
  try { (Get-Content $remMetrics -Raw | ConvertFrom-Json) | Select-Object -Last 1 } catch { $null }
}

Describe 'Week 11 Gate v3 (AI remediation signals)' {
  It '11.1 AI suggestions exist and are recent' {
    (Test-Path $sugDir) | Should Be $true
    $recent = Get-ChildItem $sugDir -Filter *.jsonl -ErrorAction SilentlyContinue |
      Where-Object { $_.LastWriteTime -gt $cutoff } | Select-Object -First 1
    ($recent -ne $null) | Should Be $true
  }
  It '11.3 Patches were generated (.diff present)' {
    (Test-Path $patchDir) | Should Be $true
    $has = Get-ChildItem $patchDir -Filter *.diff -ErrorAction SilentlyContinue | Select-Object -First 1
    ($has -ne $null) | Should Be $true
  }
  It '11.1 metrics show attempted > 0 (recent)' {
    $m = Get-LatestMetric
    if (-not $m) { $false | Should Be $true }
    else {
      $ts = [datetime]::Parse(($m.ts -replace 'Z$'))
      (($ts -gt $cutoff) -and ((0+$m.attempted) -gt 0)) | Should Be $true
    }
  }
}
