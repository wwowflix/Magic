# Magic Orchestrator v3 (ASCII-safe, drive-agnostic)
param([string]$Root = $(Get-Location).Path)
$ErrorActionPreference = "Stop"

$phasePath = Join-Path $Root "scripts\phase11"
$logDir    = Join-Path $Root "outputs\logs"
$summary   = Join-Path $logDir "master_orchestrator_summary.tsv"

New-Item -ItemType Directory -Force -Path $logDir | Out-Null

$results = @()
$ready   = Get-ChildItem -Path $phasePath -Recurse -Filter "*_READY.py" -File | Sort-Object Name
Write-Host ("Discovered {0} READY scripts under {1}" -f $ready.Count, $phasePath)

foreach ($f in $ready) {
  $rel     = $f.FullName.Substring($Root.Length).TrimStart('\')
  Write-Host ("RUN  : {0}" -f $rel)

  $outFile = Join-Path $logDir ("{0}.log" -f ($rel -replace '[\\/:\*\?""<>\|]', '_'))
  $status  = "FAIL"
  $detail  = ""

  try {
    $output = & python $f.FullName 2>&1
    $code   = $LASTEXITCODE
    $detail = ($output | Out-String).Trim()

    if ($code -eq 0 -and $detail -match "PASS") { $status = "PASS" }
    elseif ($code -eq 0)                         { $status = "OK"   }
    else                                         { $status = "FAIL" }

    Set-Content -LiteralPath $outFile -Value $detail -Encoding UTF8
    Write-Host ("  => {0} (exit={1})" -f $status, $code)
  }
  catch {
    $status = "ERROR"
    $detail = $_ | Out-String
    Set-Content -LiteralPath $outFile -Value $detail -Encoding UTF8
    Write-Host "  => ERROR"
  }

  $results += [pscustomobject]@{ script = $rel; status = $status }
}

"script`tstatus" | Set-Content -LiteralPath $summary -Encoding UTF8
$results | ForEach-Object { "{0}`t{1}" -f $_.script, $_.status } |
  Add-Content -LiteralPath $summary -Encoding UTF8

Write-Host ("Summary saved to {0}" -f $summary)
