$ErrorActionPreference='Stop'
$PSDefaultParameterValues['*:Encoding']='utf8'
$ROOT = $env:MAGIC_ROOT; if (-not $ROOT) { $ROOT = (Get-Location).Path }
$latest = Get-ChildItem (Join-Path $ROOT 'outputs\full_run') -Directory -ErrorAction SilentlyContinue |
  Sort-Object LastWriteTime -Desc | Select-Object -First 1
$master = if ($latest) { Join-Path $latest.FullName 'phase_master_summary.tsv' } else { '' }
$cutoff = (Get-Date).AddHours(-48)
$minSuccess = [double](if ($env:MIN_SUCCESS) { $env:MIN_SUCCESS } else { 60 }) # %
$strict = $env:REQUIRE_QUALITY -eq '1'

Describe 'Week 12 Gate v1 (full run quality)' {
  It '12.1 master summary exists and is recent' {
    (Test-Path $master) | Should Be $true
    ((Get-Item $master).LastWriteTime -gt $cutoff) | Should Be $true
  }
  It '12.1 has at least 1 attempted script' {
    $c = Get-Content $master
    $ok   = ($c | Select-String -SimpleMatch "`tOK`t").Count
    $fail = ($c | Select-String -SimpleMatch "`tFAIL`t").Count
    (($ok + $fail) -gt 0) | Should Be $true
  }
  It '12.1 meets success-rate threshold (if REQUIRE_QUALITY=1)' {
    $c = Get-Content $master
    $ok   = ($c | Select-String -SimpleMatch "`tOK`t").Count
    $fail = ($c | Select-String -SimpleMatch "`tFAIL`t").Count
    $att = $ok + $fail
    if ($strict -and $att -gt 0) {
      ((100.0*$ok/$att) -ge $minSuccess) | Should Be $true
    } else {
      $true | Should Be $true
    }
  }
}
