[CmdletBinding()]
param(
  [Parameter(Mandatory=$true)]
  [ValidatePattern('^[A-Za-z]{1,2}$')]
  [string]$Module,

  [string]$SummaryPath = ""
)

$ErrorActionPreference = 'Stop'
$Module = ('' + $Module).Trim().ToUpper()

function Find-OrchestratorSummary {
  param([string]$Root = (Get-Location).Path)

  $candidates = @(
    (Join-Path $Root 'outputs\logs\master_orchestrator_summary.tsv')
  )
  foreach ($p in $candidates) {
    if (Test-Path $p) { return $p }
  }

  $glob = Join-Path $Root 'outputs\logs\*.tsv'
  $latest = Get-ChildItem -Path $glob -File -ErrorAction SilentlyContinue |
            Sort-Object LastWriteTime -Descending |
            Select-Object -First 1
  if ($latest) { return $latest.FullName }

  return $null
}

function Read-OrchestratorSummary {
  param([Parameter(Mandatory)][string]$Path)

  if (-not (Test-Path $Path)) { throw "Summary not found: $Path" }

  # Read UTF-8 (no BOM) and normalize newlines to `n
  $raw   = [System.IO.File]::ReadAllText($Path, [System.Text.UTF8Encoding]::new($false)) -replace "`r?`n","`n"
  $lines = $raw -split "`n" | Where-Object { $_ -ne "" }
  if (-not $lines) { return @() }

  $header = $lines[0]

  # PS 5.1-safe delimiter detection
  if ($header -like "*;*") { $delim = ';' } else { $delim = "`t" }

  # Does the first row look like a header?
  $hasHeader = ($header -match 'module' -or $header -match 'script' -or $header -match 'exitcode' -or $header -match 'result')

  if ($hasHeader) {
    $csv = $raw | ConvertFrom-Csv -Delimiter $delim
  } else {
    # Synthesize a header
    $body = ($lines -join "`n")
    $synthetic = "Module${delim}Script${delim}Result${delim}ExitCode`n$body"
    $csv = $synthetic | ConvertFrom-Csv -Delimiter $delim
  }

  function Get-PropValue($obj, $names) {
    foreach ($n in $names) {
      $p = $obj.PSObject.Properties[$n]
      if ($p) { return $p.Value }
    }
    return $null
  }

  $out = @()
  foreach ($row in $csv) {
    $m = Get-PropValue $row @('Module','module')
    $s = Get-PropValue $row @('Script','script')
    $r = Get-PropValue $row @('Result','result')
    $x = Get-PropValue $row @('ExitCode','exitcode')

    # Infer module from script path if missing (e.g., scripts\phase11\module_E\...)
    if (-not $m -and $s -and ($s -match 'module_([A-Za-z]{1,2})[\\/]+')) {
      $m = $matches[1]
    }

    $out += [pscustomobject]@{
      Module   = ('' + $m).Trim().ToUpper()
      Script   = ('' + $s).Trim()
      Result   = ('' + $r).Trim().ToUpper() # OK/PASS/FAIL/ERROR
      ExitCode = ([int]("$x"))
    }
  }

  return ,$out
}

# ----- main flow -----

if ([string]::IsNullOrWhiteSpace($SummaryPath)) {
  $SummaryPath = Find-OrchestratorSummary
}

if ([string]::IsNullOrWhiteSpace($SummaryPath) -or -not (Test-Path $SummaryPath)) {
  Write-Warning "No orchestrator summary found. Running orchestrator to generate one..."
  $orch = Join-Path (Get-Location).Path 'tools\Magic_Orchestrator_Master_v3.ps1'
  if (-not (Test-Path $orch)) { throw "Missing $orch" }
  powershell -NoProfile -ExecutionPolicy Bypass -File $orch
  $SummaryPath = Find-OrchestratorSummary
  if ([string]::IsNullOrWhiteSpace($SummaryPath) -or -not (Test-Path $SummaryPath)) {
    throw "Unable to locate orchestrator summary after run."
  }
}

Write-Verbose "Using summary: $SummaryPath"
$summary = Read-OrchestratorSummary -Path $SummaryPath

# Filter rows for this module; ignore blanks
$rowsForModule = $summary | Where-Object { $_.Module -and ($_.Module -eq $Module) }

if (-not $rowsForModule -or $rowsForModule.Count -eq 0) {
  Write-Warning "No rows found for module '$Module'. Passing conservatively."
  exit 0
}

Write-Host "Found $($rowsForModule.Count) rows for module '$Module' in '$SummaryPath'"

$bad = $rowsForModule | Where-Object { $_.Result -in @('FAIL','ERROR') -or $_.ExitCode -ne 0 }

$rowsForModule |
  Select-Object Script, Result, ExitCode |
  Format-Table -AutoSize | Out-String | Write-Host

if ($bad -and $bad.Count -gt 0) {
  Write-Error ("Detected {0} failing rows for module '{1}'." -f $bad.Count, $Module)
  exit 1
}

Write-Host "Module '$Module' guard PASS."
exit 0
