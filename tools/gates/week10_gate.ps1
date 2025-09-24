Param(
  [int]$MinOK = 50,
  [int]$MaxFail = 5,
  [string]$LogGlob = ".\outputs\nightly_allphases_*.log"
)

$ErrorActionPreference = 'Stop'
function Fail($msg) { Write-Host "❌ $msg" -ForegroundColor Red; exit 1 }
function Pass($msg) { Write-Host "✅ $msg" -ForegroundColor Green }

# 1) Latest nightly summary
$log = Get-ChildItem $LogGlob -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Desc | Select-Object -First 1
if (-not $log) { Fail "No nightly logs found ($LogGlob)" }

$summary = (Select-String -Path $log.FullName -Pattern '^Summary: OK=(\d+)\s+FAIL=(\d+)\s+TOTAL=(\d+)').Matches
if ($summary.Count -eq 0) { Fail "No Summary line in $($log.Name)" }

$ok    = [int]$summary[0].Groups[1].Value
$fail  = [int]$summary[0].Groups[2].Value
$total = [int]$summary[0].Groups[3].Value

Write-Host ("Nightly summary: OK={0} FAIL={1} TOTAL={2}" -f $ok,$fail,$total)
if ($ok -lt $MinOK) { Fail "OK <$MinOK" }
if ($fail -gt $MaxFail) { Fail "FAIL >$MaxFail" }
Pass "Nightly thresholds met"

# 2) CI hygiene: PYTHONPATH in workflow
$wf = ".github\workflows\ci.yml"
if (-not (Test-Path $wf)) { Fail "ci.yml missing" }
$wfRaw = Get-Content $wf -Raw
if ($wfRaw -notmatch '(?ms)^\s*env:\s*[\r\n]+(\s+.+\r?\n)*\s*PYTHONPATH\s*:\s*\.' -and
    $wfRaw -notmatch 'PYTHONPATH:\s*\.') {
  Fail "PYTHONPATH=. not set in ci.yml env"
}
Pass "CI env has PYTHONPATH=."

# 3) Redundancy & dead-job checks present
$req = @(
  'scripts\phase11\module_f\11F_retry_dead_job_scanner_READY.py',
  'scripts\phase11\module_f\11F_redundancy_reducer_READY.py'
)
$missing = $req | Where-Object { -not (Test-Path $_) }
if ($missing) { Fail ("Missing Week-10 resilience scripts: {0}" -f ($missing -join ', ')) }
Pass "Resilience scripts exist"

# 4) No BOM in tracked .py
$bad = @()
$tracked = (& git ls-files *.py 2>$null)
foreach ($f in $tracked) {
  $b = [System.IO.File]::OpenRead($f)
  try {
    $buf = New-Object byte[] 3
    [void]$b.Read($buf,0,3)
    if ($buf[0] -eq 0xEF -and $buf[1] -eq 0xBB -and $buf[2] -eq 0xBF) { $bad += $f }
  } finally { $b.Dispose() }
}
if ($bad.Count -gt 0) { Fail ("Files with BOM: {0}" -f ($bad -join ', ')) }
Pass "No BOM found in .py files"

Write-Host "`n✅ Week 10 gate passed." -ForegroundColor Green
exit 0
