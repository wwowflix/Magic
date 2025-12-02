# === MAGIC Where-Am-I Status v2 ===

$ErrorActionPreference = 'Stop'

# Go to repo root
Set-Location E:\MAGIC

# Try to activate venv if available
if (Test-Path ".\venv\Scripts\Activate") {
  . .\venv\Scripts\Activate
}

# Ensure output folders exist
if (-not (Test-Path .\outputs\reports)) { New-Item -ItemType Directory -Force -Path .\outputs\reports | Out-Null }
if (-not (Test-Path .\outputs\proofs))  { New-Item -ItemType Directory -Force -Path .\outputs\proofs  | Out-Null }

$now     = Get-Date -Format "yyyyMMdd_HHmmss"
$outTsv  = ".\outputs\reports\where_am_i_magic_$now.tsv"
$outJson = ".\outputs\reports\where_am_i_magic_$now.json"
$rows    = @()   # collection of result rows

function Add-Row($Stage,$Check,$Pass,$Evidence,$Notes) {
  $rows += [pscustomobject]@{
    Stage    = $Stage
    Check    = $Check
    Status   = if ($Pass) { 'PASS' } else { 'FAIL' }
    Evidence = $Evidence
    Notes    = $Notes
  }
}

Write-Host "=== MAGIC – WHERE AM I NOW? ($now) ==="
Write-Host ""

# ---- GIT OVERALL STATUS ----
try { $branch = (git rev-parse --abbrev-ref HEAD).Trim() } catch { $branch = $null }

try { $upstream = (git rev-parse --abbrev-ref --symbolic-full-name "@{u}") 2>$null } catch { $upstream = $null }

try {
  $aheadBehindRaw = (git rev-list --left-right --count HEAD...@{u}) 2>$null
  if ($aheadBehindRaw) {
    $parts  = $aheadBehindRaw -split "\s+"
    $ahead  = [int]$parts[0]
    $behind = [int]$parts[1]
  } else {
    $ahead = 0; $behind = 0
  }
} catch { $ahead = 0; $behind = 0 }

try {
  $dirtyLines = (git status --porcelain) 2>$null
  $dirtyCount = if ($dirtyLines) { ($dirtyLines | Measure-Object -Line).Lines } else { 0 }
} catch { $dirtyCount = -1 }

try {
  $lastCommit = (git log -1 --pretty="format:%h|%ci|%s") 2>$null
} catch { $lastCommit = $null }

Add-Row 'GIT' 'Current branch' ($branch -ne $null) $branch ''
Add-Row 'GIT' 'Has upstream tracking' ($upstream -ne $null -and $upstream -ne '') $upstream 'Fail ⇒ no remote tracking branch'
Add-Row 'GIT' 'Ahead/Behind upstream' $true ("ahead=$ahead; behind=$behind") 'Non-zero = diverged from origin'
Add-Row 'GIT' 'Working tree clean' ($dirtyCount -eq 0) ("dirty_lines=$dirtyCount") 'Fail ⇒ unstaged/uncommitted changes'
Add-Row 'GIT' 'Last commit' ($lastCommit -ne $null) $lastCommit ''

# ---- MAGIC STRUCTURE & SCRIPTS ----
$readyFiles = Get-ChildItem -Recurse -File -Filter "*_READY.py" .\scripts -ErrorAction SilentlyContinue
$tiny = @()
foreach($f in $readyFiles){
  try {
    $content = Get-Content -LiteralPath $f.FullName -Raw -ErrorAction Stop
    if ($content.Trim().Length -lt 20) { $tiny += $f.FullName }
  } catch {}
}
Add-Row 'MAGIC' 'READY.py count' ($readyFiles.Count -gt 0) "count=$($readyFiles.Count)" 'Expect ≈ 900 when fully scaffolded'
Add-Row 'MAGIC' 'No tiny/empty READY.py' ($tiny.Count -eq 0) "tiny=$($tiny.Count)" 'Fail ⇒ some scripts still skeleton placeholders'

# Phase 11 folder check
$phase11Dir    = ".\scripts\phase11"
$phase11Exists = Test-Path $phase11Dir
if ($phase11Exists) {
  $modules = Get-ChildItem $phase11Dir -Directory -ErrorAction SilentlyContinue
  Add-Row 'MAGIC' 'Phase 11 folder exists' $true $phase11Dir ("modules=" + $modules.Count)
} else {
  Add-Row 'MAGIC' 'Phase 11 folder exists' $false $phase11Dir 'Missing Phase 11 scripts folder'
}

# Orchestrator / Phase 11 reports
$orchestratorLog = ".\outputs\logs\master_orchestrator_summary.tsv"
$phase11Summary  = ".\outputs\reports\phase11_full_latest.tsv"
Add-Row 'MAGIC' 'Orchestrator summary present' (Test-Path $orchestratorLog) $orchestratorLog ''
Add-Row 'MAGIC' 'Phase 11 latest TSV present' (Test-Path $phase11Summary) $phase11Summary ''

# ---- TESTS / SMOKES (LIGHT CHECK) ----
try {
  if (Test-Path ".\tests\smoke\test_phase11_param_ok.py") {
    Write-Host "Running quick Phase-11 param smoke (pytest -q tests/smoke/test_phase11_param_ok.py -q) ..." -ForegroundColor Cyan
    $env:PYTEST_DISABLE_PLUGIN_AUTOLOAD = "1"
    pytest -q tests/smoke/test_phase11_param_ok.py -q
    $ok = ($LASTEXITCODE -eq 0)
    Add-Row 'TESTS' 'Phase11 param smoke' $ok ("exit=$LASTEXITCODE") ''
  } else {
    Add-Row 'TESTS' 'Phase11 param smoke test file present' $false 'tests/smoke/test_phase11_param_ok.py' 'Test file missing'
  }
} catch {
  Add-Row 'TESTS' 'Phase11 param smoke' $false '' $_.Exception.Message
}

# ---- RELEASE ARTIFACTS (if present) ----
$magicFullStatus = ".\outputs\reports\magic_full_status.json"
$cleanupPlan     = ".\outputs\reports\cleanup_plan.tsv"
$releaseZip      = Get-ChildItem ".\backups" -Filter "release_v1.0.zip" -ErrorAction SilentlyContinue

Add-Row 'RELEASE' 'magic_full_status.json present' (Test-Path $magicFullStatus) $magicFullStatus ''
Add-Row 'RELEASE' 'cleanup_plan.tsv present' (Test-Path $cleanupPlan) $cleanupPlan ''
Add-Row 'RELEASE' 'release_v1.0.zip present' ($releaseZip -ne $null) ($releaseZip.FullName) ''

# ---- WRITE TSV & JSON ----
$rows | ConvertTo-Csv -Delimiter "`t" -NoTypeInformation | Set-Content -LiteralPath $outTsv -Encoding utf8

$summary = [ordered]@{
  generated_at = (Get-Date).ToString("s")
  git = [ordered]@{
    branch       = $branch
    upstream     = $upstream
    ahead        = $ahead
    behind       = $behind
    dirty_lines  = $dirtyCount
    last_commit  = $lastCommit
  }
  totals = [ordered]@{
    pass = ($rows | Where-Object {$_.Status -eq 'PASS'}).Count
    fail = ($rows | Where-Object {$_.Status -eq 'FAIL'}).Count
  }
  details = $rows
}

$summary | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $outJson -Encoding utf8

# Debug: show all rows
Write-Host ""
Write-Host "Row debug: total rows collected = $($rows.Count)"
$rows | Select-Object Stage, Check, Status | Format-Table -AutoSize
Write-Host ""

Write-Host "=== SUMMARY ==="
Write-Host ("PASS: " + $summary.totals.pass + "  FAIL: " + $summary.totals.fail)
Write-Host ("Branch : " + $summary.git.branch)
$up = if ([string]::IsNullOrEmpty($summary.git.upstream)) { '<none>' } else { $summary.git.upstream }
Write-Host ("Upstream: " + $up)
Write-Host ("Ahead/Behind: " + "ahead=" + $summary.git.ahead + "; behind=" + $summary.git.behind)
Write-Host ("Dirty lines: " + $summary.git.dirty_lines)
Write-Host ""
Write-Host "TSV : $outTsv"
Write-Host "JSON: $outJson"
Write-Host "Done."
