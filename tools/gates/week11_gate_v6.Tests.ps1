$ErrorActionPreference='Stop'
$PSDefaultParameterValues['*:Encoding']='utf8'
$ROOT = $env:MAGIC_ROOT; if (-not $ROOT) { $ROOT = (Get-Location).Path }
$alerts = Join-Path $ROOT 'outputs\remediation\alerts_sent.jsonl'
$cutoff = (Get-Date).AddHours(-48)

function Get-LastAlert {
  if (-not (Test-Path $alerts)) { return $null }
  $line = Get-Content $alerts -Tail 1 -ErrorAction SilentlyContinue
  if (-not $line) { return $null }
  try { return $line | ConvertFrom-Json } catch { return $null }
}

Describe 'Week 11 Gate v6 (alerts)' {
  It '11.4 alerts_sent.jsonl exists and is recent' {
    (Test-Path $alerts) | Should Be $true
    $last = Get-LastAlert
    if (-not $last) { $false | Should Be $true }
    else {
      $ts = [datetime]::Parse(($last.ts -replace 'Z$'))
      ($ts -gt $cutoff) | Should Be $true
    }
  }
  It '11.4 at least one channel entry present (github/notion; dry-run allowed)' {
    $last = Get-LastAlert
    if (-not $last) { $false | Should Be $true }
    else {
      $chs = @($last.channels)
      ($chs.Count -gt 0) | Should Be $true
    }
  }
}
