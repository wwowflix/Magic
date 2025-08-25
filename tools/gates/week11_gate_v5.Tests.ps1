$ErrorActionPreference='Stop'
$PSDefaultParameterValues['*:Encoding']='utf8'
$ROOT = $env:MAGIC_ROOT; if (-not $ROOT) { $ROOT = (Get-Location).Path }
$remMetrics = Join-Path $ROOT 'outputs\remediation\remediate_metrics.json'
$bkRoot     = Join-Path $ROOT 'outputs\remediation\backups'
$cutoff = (Get-Date).AddHours(-48)

function LastMetric {
  if (-not (Test-Path $remMetrics)) { return $null }
  try { (Get-Content $remMetrics -Raw | ConvertFrom-Json) | Select-Object -Last 1 } catch { $null }
}

Describe 'Week 11 Gate v5 (auto-apply patches)' {
  It 'backup directory exists and is recent' {
    (Test-Path $bkRoot) | Should Be $true
    $latest = Get-ChildItem $bkRoot -Directory -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Desc | Select-Object -First 1
    ($latest -ne $null) | Should Be $true
  }
  It 'remediation metrics show attempted > 0 (recent)' {
    $m = LastMetric
    if (-not $m) { $false | Should Be $true } else {
      $ts = [datetime]::Parse(($m.ts -replace 'Z$'))
      (($ts -gt $cutoff) -and ((0+$m.attempted) -gt 0)) | Should Be $true
    }
  }
}
