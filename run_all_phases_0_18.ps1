# === MAGIC All-Phase Execution Runner (0–18) ===
# Runs self_healing_runner_v5.py phase-by-phase and records a master summary.
# v5 supports: --manifest --phases --modules --list --dry-run --summary-dir
# It does NOT take --auto-heal or --max-retries (handled inside the runner).

param(
  [string]$RunnerPath   = ".\self_healing_runner_v5.py",
  [string]$ManifestPath = ".\phase_manifest.json",
  [string]$PythonExe    = ".\venv\Scripts\python.exe",
  [int[]] $Phases       = (0..18),
  [switch]$DryRun
)

$ErrorActionPreference = "Stop"
$root = Get-Location
$summaryDir = Join-Path $root "outputs\summaries"
New-Item -ItemType Directory -Force -Path $summaryDir | Out-Null

function Row($phase,$status,$cmd,$summary){
  [pscustomobject]@{
    Timestamp = (Get-Date).ToString("s")
    Phase     = $phase
    Status    = $status
    Command   = $cmd
    SummaryTSV= $summary
  }
}

# sanity checks
if (-not (Test-Path $RunnerPath))   { Write-Error "Runner not found: $RunnerPath" }
if (-not (Test-Path $ManifestPath)) { Write-Error "Manifest not found: $ManifestPath" }
if (-not (Test-Path $PythonExe))    { $PythonExe = "python" }  # fallback to global python

$rows = @()

foreach ($p in $Phases) {
  Write-Host "`n=== Phase $p ===" -ForegroundColor Cyan

  $args = @("$RunnerPath","--manifest",$ManifestPath,"--phases",$p,"--summary-dir",$summaryDir)
  if ($DryRun) { $args += "--dry-run" }

  $cmdDisp = "$PythonExe " + ($args -join ' ')
  Write-Host $cmdDisp -ForegroundColor DarkGray

  # invoke
  & $PythonExe @args
  $exitCode = $LASTEXITCODE

  # try to locate a summary file for this phase (last written TSV in summaryDir)
  $latestSummary = Get-ChildItem $summaryDir -Filter "*.tsv" -ErrorAction SilentlyContinue |
                   Sort-Object LastWriteTime -Descending | Select-Object -First 1
  $summaryPath = if ($latestSummary) { $latestSummary.FullName } else { "" }

  if ($exitCode -eq 0) {
    Write-Host "Phase $p: OK" -ForegroundColor Green
    $rows += Row $p "OK" $cmdDisp $summaryPath
  } else {
    Write-Host "Phase $p: FAIL (exit $exitCode)" -ForegroundColor Red
    $rows += Row $p "FAIL($exitCode)" $cmdDisp $summaryPath
  }
}

# write master summary
$stamp = (Get-Date).ToString("yyyyMMdd_HHmmss")
$master = Join-Path $summaryDir "master_run_0_18_$stamp.tsv"
$rows | Export-Csv -NoTypeInformation -Delimiter "`t" -Path $master

# pretty print roll-up
$ok   = ($rows | Where-Object {$_.Status -like "OK"}).Count
$fail = ($rows | Where-Object {$_.Status -like "FAIL*"}).Count
Write-Host "`n======== MASTER RUN SUMMARY ========" -ForegroundColor Yellow
Write-Host ("OK   : {0}" -f $ok)
Write-Host ("FAIL : {0}" -f $fail)
Write-Host ("TSV  : {0}" -f $master)
if ($fail -gt 0) {
  Write-Host "Tip: open the per-phase summary (SummaryTSV) and the logs under outputs\logs\phaseX_module_Y\ for details." -ForegroundColor DarkYellow
}
