$ErrorActionPreference='Stop'
$PSDefaultParameterValues['*:Encoding']='utf8'
$ROOT = $env:MAGIC_ROOT; if (-not $ROOT) { $ROOT = (Get-Location).Path }
$prio = Join-Path $ROOT 'outputs\remediation\prioritized_failures.json'
$ord  = Join-Path $ROOT 'outputs\remediation\ordered_manifest.json'
$run  = Join-Path $ROOT 'outputs\remediation\ordering_run.json'
$cutoff = (Get-Date).AddHours(-48)

function Normalize([string]$s) {
  if (-not $s) { return '' }
  $b = [System.IO.Path]::GetFileNameWithoutExtension($s).ToLower()
  return ($b -replace '_(ready|draft|hold)$','')
}

Describe 'Week 11 Gate v4 (prioritization)' {
  It 'ordered_manifest.json exists and is recent' {
    (Test-Path $ord) | Should Be $true
    ((Get-Item $ord).LastWriteTime -gt $cutoff) | Should Be $true
  }
  It 'prioritized items appear first when available' {
    $p = @()
    if (Test-Path $prio) { $p = Get-Content $prio -Raw | ConvertFrom-Json }
    if ($p.Count -gt 0) {
      $o = Get-Content $ord -Raw | ConvertFrom-Json
      $want = @()
      foreach($x in $p) { $fn = $x.final_filename; if (-not $fn) { $fn=$x.filename }; if ($fn) { $want += (Normalize $fn) } }
      $got = @(); foreach($row in $o[0..([Math]::Min($o.Count,$want.Count)-1)]) { $f=$row.final_filename; if (-not $f) { $f=$row.filename }; $got += (Normalize $f) }
      # allow order equality ignoring extras
      ($got -eq $want[0..($got.Count-1)]) | Should Be $true
    } else {
      $true | Should Be $true
    }
  }
}
