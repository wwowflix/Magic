<#
  magic_scan_status.ps1
  Full repo scan → weeks 1–12 status + per-phase completion + infra signals
  Outputs: outputs\reports\magic_scan_summary.md / .tsv / .json
#>

param([string]$Root = "D:\MAGIC")
$ErrorActionPreference = 'Stop'
if (-not (Test-Path $Root)) { Write-Host "Root path not found: $Root" -ForegroundColor Red; exit 2 }
Set-Location $Root

# -----------------------------
# IO helpers
# -----------------------------
$ReportDir = Join-Path $Root "outputs\reports"
if (-not (Test-Path $ReportDir)) { New-Item -ItemType Directory -Force -Path $ReportDir | Out-Null }
$TSV  = Join-Path $ReportDir "magic_scan_summary.tsv"
$MD   = Join-Path $ReportDir "magic_scan_summary.md"
$JSON = Join-Path $ReportDir "magic_scan_summary.json"

function Exists($p){ Test-Path -LiteralPath $p }
function Files($glob){ try { Get-ChildItem -Path $glob -Recurse -File -ErrorAction SilentlyContinue } catch { @() } }
function CountFiles($p,$f="*"){ if(-not(Test-Path $p)){0}else{ (Get-ChildItem $p -Recurse -File -Filter $f -ErrorAction SilentlyContinue).Count } }
function ReadText($p){
  try { return [System.IO.File]::ReadAllText($p,[System.Text.Encoding]::UTF8) } catch {
    try { return Get-Content $p -Raw -Encoding UTF8 } catch { return "" }
  }
}
function AnyYamlHas($pattern){
  $paths = @(".github\workflows\*.yml",".github\workflows\*.yaml") | ForEach-Object { Join-Path $Root $_ }
  $yml = foreach($p in $paths){ Files $p }
  foreach($f in $yml){ if ((ReadText $f.FullName) -like "*$pattern*"){ return $true } }
  return $false
}

# -----------------------------
# Evidence snapshot
# -----------------------------
$scriptsDir   = Join-Path $Root "scripts"
$scriptsReady = Files (Join-Path $scriptsDir "*_READY.py")
$scriptCount  = @($scriptsReady).Count

$preCommit    = Exists (Join-Path $Root ".pre-commit-config.yaml")
$workflowsDir = Join-Path $Root ".github\workflows"
$hasWorkflows = Exists $workflowsDir
$ciAny        = AnyYamlHas "on:"
$ciNightly    = (AnyYamlHas "schedule:") -or (AnyYamlHas "cron:")

$testsDir     = Join-Path $Root "tests"
$hasTests     = Exists $testsDir
$testCount    = CountFiles $testsDir "*.py"
$pytestIni    = Exists (Join-Path $Root "pytest.ini") -or Exists (Join-Path $Root "pyproject.toml")
$pytestInCI   = AnyYamlHas "pytest"

$logsDirs     = @("outputs\logs","logs") | ForEach-Object { Join-Path $Root $_ }
$logCount     = 0; foreach($d in $logsDirs){ $logCount += CountFiles $d "*.*" }

$reportsDir   = Join-Path $Root "outputs\reports"
$reportsCount = CountFiles $reportsDir "*.*"
$metricsTsv   = Files (Join-Path $reportsDir "metrics*.tsv")
$metricsCount = @($metricsTsv).Count

$backupsDir   = Join-Path $Root "backups"
$backupsCount = CountFiles $backupsDir "*.*"

# Aggregate source text safely (wrap pipeline before -join)
$toolFiles = @()
$toolPs1 = Files (Join-Path $Root "tools\**\*.ps1"); if ($toolPs1) { $toolFiles += $toolPs1 }
$toolPy  = Files (Join-Path $Root "tools\**\*.py");  if ($toolPy)  { $toolFiles += $toolPy  }
$toolsText  = (($toolFiles  | ForEach-Object { ReadText $_.FullName }) -join "`n")

$agentFiles = @()
$agentPs1 = Files (Join-Path $Root "agents\**\*.ps1"); if ($agentPs1) { $agentFiles += $agentPs1 }
$agentPy  = Files (Join-Path $Root "agents\**\*.py");  if ($agentPy)  { $agentFiles += $agentPy  }
$agentsText = (($agentFiles | ForEach-Object { ReadText $_.FullName }) -join "`n")

$runnerText = ""
$runnerCandidates = @(
  "self_healing_runner_v5.py","self_healing_runner_v4.4.py","self_healing_runner_v4.3.py",
  "tools\**\*runner*.py","agents\meta\**\*runner*.py"
) | ForEach-Object { Join-Path $Root $_ } | ForEach-Object { Files $_ }
foreach($rc in $runnerCandidates){ $runnerText += "`n" + (ReadText $rc.FullName) }

# -----------------------------
# Placeholder detection & phase inference
# -----------------------------
function IsPlaceholder($file) {
  try {
    $len = (Get-Item $file.FullName).Length
    if ($len -lt 140) { return $true }
    $t = ReadText $file.FullName
    if ($t -match '(?i)placeholder') { return $true }
    # collapse lines; regex matches """...""" or '''...''' + pass
    $t2 = ($t -replace "(\r?\n)+"," " ).Trim()
    $pattern = "^\s*(?:(?:""{3})|(?:'{3})).*?(?:(?:""{3})|(?:'{3}))\s*pass\s*$"
    if ($t2 -match $pattern) { return $true }
    return $false
  } catch { return $true }
}

$rePhaseDir  = [regex]'[\\/]{1}phase(?<num>\d+)[\\/]'
$reModuleDir = [regex]'[\\/]module_(?<mod>[A-Z])[\\/]'
$reFilePref  = [regex]'^(?<num>\d{2})(?<mod>[A-Z])_'

function InferPhaseModule($file) {
  $p = $file.FullName; $fn = $file.Name
  $phaseNum = $null; $mod = $null
  $m1 = $rePhaseDir.Match($p);  if($m1.Success){ $phaseNum = [int]$m1.Groups['num'].Value }
  $m2 = $reModuleDir.Match($p); if($m2.Success){ $mod = $m2.Groups['mod'].Value.ToUpper() }
  if (-not $phaseNum -or -not $mod) {
    $m3 = $reFilePref.Match($fn)
    if($m3.Success){ if(-not $phaseNum){ $phaseNum = [int]$m3.Groups['num'].Value }; if(-not $mod){ $mod = $m3.Groups['mod'].Value.ToUpper() } }
  }
  return @{ PhaseNumber = $phaseNum; Module = $mod }
}

# Per-phase stats
$phaseStats = @{}
foreach($f in $scriptsReady){
  $inf = InferPhaseModule $f
  $pn  = if($inf.PhaseNumber){ [int]$inf.PhaseNumber } else { -1 }
  $mod = if($inf.Module){ $inf.Module } else { "_" }
  if(-not $phaseStats.ContainsKey($pn)){ $phaseStats[$pn] = @{ total = 0; impl = 0; placeholder = 0; modules = @{} } }
  $phaseStats[$pn].total++
  $ph = IsPlaceholder $f
  if($ph){ $phaseStats[$pn].placeholder++ } else { $phaseStats[$pn].impl++ }
  if(-not $phaseStats[$pn].modules.ContainsKey($mod)){ $phaseStats[$pn].modules[$mod] = @{ total = 0; impl = 0; placeholder = 0 } }
  $phaseStats[$pn].modules[$mod].total++
  if($ph){ $phaseStats[$pn].modules[$mod].placeholder++ } else { $phaseStats[$pn].modules[$mod].impl++ }
}

# -----------------------------
# Week statuses
# -----------------------------
$manifest = (Files (Join-Path $Root "*manifest*.json") | Select-Object -First 1)
$w1 = if($scriptCount -gt 0 -and $manifest){ "Done" } elseif($scriptCount -gt 0){ "In-Progress (manifest missing)" } else { "Not Started" }
$w2 = if($logCount -gt 0){ "Done" } else { "In-Progress" }
$hasSelfHeal = ($runnerText + $toolsText + $agentsText) -match "FileNotFoundError|ImportError|UnicodeEncodeError|ensure_placeholder|create_dummy|auto[_-]?install|remediate|fallback"
$w3 = if($hasSelfHeal){ "Done" } else { "In-Progress" }
$w4 = if($preCommit -and $hasWorkflows -and $ciAny){ "Done (may be noisy)" } else { "In-Progress" }

$phase11Proof = @()
$phase11Proof += (Files (Join-Path $Root "outputs\**\*phase11*.*"))
$phase11Proof += (Files (Join-Path $Root "logs\**\*phase11*.*"))
$phase11Proof += (Files (Join-Path $Root "outputs\reports\**\*phase11*summary*.tsv"))
$w5 = if($phase11Proof.Count -gt 0){ "Done" } elseif($logCount -gt 0){ "In-Progress" } else { "Planned" }

$hasPyParallel = $runnerText -match "concurrent\.futures|ThreadPoolExecutor|ProcessPoolExecutor|multiprocessing|asyncio\.gather"
$hasPsParallel = ($toolsText + $agentsText) -match "Start-Job|ForEach-Object\s*-Parallel|Start-Process|Invoke-Parallel"
$w6 = if($hasPyParallel -or $hasPsParallel){ "In-Progress" } else { "Blocked (no parallel signals)" }

$w7 = if($hasTests -and $testCount -gt 0 -and ($pytestInCI -or $pytestIni)){ "In-Progress" } else { "Not Started" }

$metricsSignals = 0
if($runnerText -match "prometheus_client|statsd|emit_metric|METRIC"){ $metricsSignals++ }
if($toolsText -match "(?i)notion"){ $metricsSignals++ }
if($metricsCount -gt 0 -or (CountFiles $reportsDir "*.tsv") -gt 5){ $metricsSignals++ }
$w8 = if($metricsSignals -gt 0){ "In-Progress" } else { "Not Started" }

$w9  = if($ciNightly){ "In-Progress" } else { "Not Started" }
$w10 = if($backupsCount -gt 0){ "In-Progress" } else { "Not Started" }
$w11Hits = @(Files (Join-Path $Root "tools\**\*.*") | Where-Object { $_.Name -match "patch|healer|auto[-_]?fix|sanity|post[-_]?mortem|fix_ready" }).Count
$w11 = if($w11Hits -gt 0){ "In-Progress" } else { "Not Started" }
$docHits = @(Files (Join-Path $Root "docs\**\*.*"); Files (Join-Path $Root "*README*.md"); Files (Join-Path $Root "outputs\reports\**\*.md")) | Where-Object { $_.Name -match "(?i)handoff|production|dashboard|readme|overview|magic" }
$w12 = if($docHits.Count -gt 0 -and $ciNightly){ "In-Progress" } elseif($docHits.Count -gt 0){ "Planned (docs exist)" } else { "Planned" }

# -----------------------------
# Build output objects
# -----------------------------
$weeks = @(
  @{Week=1;  Step="Inventory & Foundation";      Status=$w1;  Notes=("scripts:{0}; manifest:{1}" -f $scriptCount, $(if($manifest){$manifest.Name}else{"missing"})) },
  @{Week=2;  Step="Logging & Retry";             Status=$w2;  Notes=("logs:{0}" -f $logCount) },
  @{Week=3;  Step="Self-Healing Basics";         Status=$w3;  Notes=("self-heal:{0}" -f $hasSelfHeal) },
  @{Week=4;  Step="CI/CD Integration";           Status=$w4;  Notes=("pre-commit:{0}; workflows:{1}; triggers:{2}" -f $preCommit,$hasWorkflows,$ciAny) },
  @{Week=5;  Step="Stress Test Rollout";         Status=$w5;  Notes=("phase11 proofs:{0}; total logs:{1}" -f $phase11Proof.Count,$logCount) },
  @{Week=6;  Step="Expansion & Parallelization"; Status=$w6;  Notes=("py-parallel:{0}; ps-parallel:{1}" -f $hasPyParallel,$hasPsParallel) },
  @{Week=7;  Step="Testing Layer";               Status=$w7;  Notes=("tests:{0} ({1}); pytestCI:{2}; cfg:{3}" -f $hasTests,$testCount,$pytestInCI,$pytestIni) },
  @{Week=8;  Step="Metrics & Monitoring";        Status=$w8;  Notes=("metrics signals:{0}; metrics files:{1}" -f $metricsSignals,$metricsCount) },
  @{Week=9;  Step="Nightly Full Runs";           Status=$w9;  Notes=("nightly:{0}" -f $ciNightly) },
  @{Week=10; Step="Backup & Failover";           Status=$w10; Notes=("backup files:{0}" -f $backupsCount) },
  @{Week=11; Step="Patching & Post-Mortems";     Status=$w11; Notes=("patcher tools:{0}" -f $w11Hits) },
  @{Week=12; Step="Final Production Handoff";    Status=$w12; Notes=("docs:{0}; nightly:{1}" -f $docHits.Count,$ciNightly) }
)

$phaseRows = @()
foreach($k in ($phaseStats.Keys | Sort-Object)){
  $ps = $phaseStats[$k]
  $pct = if($ps.total -gt 0){ [math]::Round(100.0 * $ps.impl / $ps.total, 1) } else { 0 }
  $phaseRows += [PSCustomObject]@{
    Phase = $k; Total = $ps.total; Implemented = $ps.impl; Placeholder = $ps.placeholder; CompletionPct = "$pct%"
  }
}

# --- SYNC: recompute final labels and push into $weeks before writing outputs

# Recompute “Done” for Weeks 6–12 from receipts (idempotent; keeps existing values if conditions not met)
try {
  if ($hasPyParallel -and $hasPsParallel) { $w6  = "Done" }
  if ($hasTests -and $testCount -gt 0 -and ($pytestInCI -or $pytestIni)) {
    $pytestReceipt = Join-Path $reportsDir "pytest_last.txt"
    if (Test-Path $pytestReceipt) {
      $pytestStatus = (Get-Content $pytestReceipt -Raw)
      if ($pytestStatus -like "*PASS*") { $w7 = "Done" }
    }
  }
  if ($metricsSignals -gt 0 -and (Get-ChildItem (Join-Path $reportsDir "metrics*.tsv") -ErrorAction SilentlyContinue)) { $w8 = "Done" }
  if ($ciNightly -or (Get-ChildItem (Join-Path $reportsDir "nightly_*") -ErrorAction SilentlyContinue)) { $w9 = "Done" }
  if ($backupsCount -gt 0 -and (Test-Path (Join-Path $reportsDir "restore_smoke_ok.txt"))) { $w10 = "Done" }
  if ($w11Hits -gt 0 -and (Get-ChildItem (Join-Path $reportsDir "*post*mor*em*.md") -ErrorAction SilentlyContinue)) { $w11 = "Done" }
  if ($docHits.Count -gt 0 -and $ciNightly -and (Test-Path (Join-Path $Root "docs\PRODUCTION_HANDOFF.md"))) { $w12 = "Done" }
} catch { }

# Push the final labels into the already-built $weeks array
if ($weeks) {
  foreach ($row in $weeks) {
    switch ($row.Week) {
      6  { $row.Status = $w6 }
      7  { $row.Status = $w7 }
      8  { $row.Status = $w8 }
      9  { $row.Status = $w9 }
      10 { $row.Status = $w10 }
      11 { $row.Status = $w11 }
      12 { $row.Status = $w12 }
    }
  }
}
# --- WEEK 12 OVERRIDE (simple & definitive)
try {
  $handoffPath = Join-Path $Root "docs\PRODUCTION_HANDOFF.md"
  if ($ciNightly -and (Test-Path $handoffPath)) {
    $w12 = "Done"
  }
} catch { }
# -----------------------------
# Write TSV
# -----------------------------
"Week`tStep`tStatus`tNotes" | Out-File -FilePath $TSV -Encoding utf8
foreach($w in $weeks){ ("{0}`t{1}`t{2}`t{3}" -f $w.Week,$w.Step,$w.Status,$w.Notes) | Out-File -FilePath $TSV -Append -Encoding utf8 }
"`nPhase`tTotal`tImplemented`tPlaceholder`tCompletionPct" | Out-File -FilePath $TSV -Append -Encoding utf8
foreach($pr in $phaseRows){ ("{0}`t{1}`t{2}`t{3}`t{4}" -f $pr.Phase,$pr.Total,$pr.Implemented,$pr.Placeholder,$pr.CompletionPct) | Out-File -FilePath $TSV -Append -Encoding utf8 }

# -----------------------------
# Write Markdown
# -----------------------------
@"
# MAGIC – Full Scan Summary

## Weeks 1–12 Status
| Week | Step | Status | Notes |
|-----:|------|--------|-------|
"@ | Out-File -FilePath $MD -Encoding utf8
foreach($w in $weeks){
  ("| {0} | {1} | {2} | {3} |" -f $w.Week,$w.Step,$w.Status,($w.Notes -replace "\|","/")) |
    Out-File -FilePath $MD -Append -Encoding utf8
}
@"

## Per-Phase Completion (Implemented vs Placeholder)
| Phase | Total | Implemented | Placeholder | Completion % |
|-----:|------:|------------:|------------:|-------------:|
"@ | Out-File -FilePath $MD -Append -Encoding utf8
foreach($pr in ($phaseRows | Sort-Object Phase)){
  ("| {0} | {1} | {2} | {3} | {4} |" -f $pr.Phase,$pr.Total,$pr.Implemented,$pr.Placeholder,$pr.CompletionPct) |
    Out-File -FilePath $MD -Append -Encoding utf8
}
@"

## Infra Signals
- pre-commit: $preCommit
- workflows present: $hasWorkflows
- CI triggers (on:): $ciAny
- Nightly schedule: $ciNightly
- tests dir: $hasTests ($testCount files)
- pytest in CI: $pytestInCI
- pytest cfg present: $pytestIni
- logs total: $logCount
- reports total: $reportsCount
- metrics TSV files: $metricsCount
- backups files: $backupsCount

"@ | Out-File -FilePath $MD -Append -Encoding utf8

# -----------------------------
# Write JSON
# -----------------------------
$payload = [PSCustomObject]@{
  weeks  = $weeks
  phases = $phaseRows
  counts = @{ scripts_ready=$scriptCount; logs=$logCount; reports=$reportsCount; metrics_files=$metricsCount; backups=$backupsCount }
  signals= @{ pre_commit=$preCommit; workflows=$hasWorkflows; ci_triggers=$ciAny; nightly=$ciNightly; has_tests=$hasTests; test_count=$testCount; pytest_in_ci=$pytestInCI; pytest_cfg=$pytestIni; self_heal=$hasSelfHeal; py_parallel=$hasPyParallel; ps_parallel=$hasPsParallel }
}
$payload | ConvertTo-Json -Depth 6 | Out-File -FilePath $JSON -Encoding utf8

# -----------------------------
# # -----------------------------
# OVERRIDES: mark Weeks 6–12 as Done when receipts exist
# --- SYNC: push final labels into $weeks table before printing
if ($weeks) {
  foreach ($row in $weeks) {
    switch ($row.Week) {
      6  { $row.Status = $w6 }
      7  { $row.Status = $w7 }
      8  { $row.Status = $w8 }
      9  { $row.Status = $w9 }
      10 { $row.Status = $w10 }
      11 { $row.Status = $w11 }
      12 { $row.Status = $w12 }
    }
  }
}

# (We keep original logic; this only upgrades final labels.)
# -----------------------------
# Variables used below already exist earlier in the script:
#   $hasPyParallel, $hasPsParallel, $hasParallel
#   $hasTests, $testCount, $pytestInCI, $pytestIni
#   $reportsDir, $ciNightly, $backupsCount, $w11Hits
#   $docHits, $metricsSignals

# Week 6: Done if BOTH Python and PowerShell parallel signals exist
if ($hasPyParallel -and $hasPsParallel) { $w6 = "Done" }

# Week 7: Done if tests present + pytest wired + last pytest run PASS receipt exists
if ($hasTests -and $testCount -gt 0 -and ($pytestInCI -or $pytestIni)) {
  $pytestReceipt = Join-Path $reportsDir "pytest_last.txt"
  if (Test-Path $pytestReceipt) {
    $pytestStatus = (Get-Content $pytestReceipt -Raw)
    if ($pytestStatus -like "*PASS*") { $w7 = "Done" }
  }
}

# Week 8: Done if metrics signals > 0 and a metrics TSV exists
if ($metricsSignals -gt 0 -and (Get-ChildItem (Join-Path $reportsDir "metrics*.tsv") -ErrorAction SilentlyContinue)) {
  $w8 = "Done"
}

# Week 9: Done if nightly schedule present OR any nightly_* stamp exists
if ($ciNightly -or (Get-ChildItem (Join-Path $reportsDir "nightly_*") -ErrorAction SilentlyContinue)) {
  $w9 = "Done"
}

# Week 10: Done if backups exist AND restore smoke receipt exists
if ($backupsCount -gt 0 -and (Test-Path (Join-Path $reportsDir "restore_smoke_ok.txt"))) {
  $w10 = "Done"
}

# Week 11: Done if patcher/healer tools exist AND any post-mortem md exists
if ($w11Hits -gt 0 -and (Get-ChildItem (Join-Path $reportsDir "*post*mor*em*.md") -ErrorAction SilentlyContinue)) {
  $w11 = "Done"
}

# Week 12: Done if docs exist + nightly true + PRODUCTION_HANDOFF.md exists
if ($docHits.Count -gt 0 -and $ciNightly -and (Test-Path (Join-Path $Root "docs\PRODUCTION_HANDOFF.md"))) {
  $w12 = "Done"
}
# -----------------------------
# Console output
# -----------------------------
Write-Host "`n=== MAGIC – Full Scan Summary ===" -ForegroundColor Cyan
$weeks | Format-Table -AutoSize
Write-Host ""
$phaseRows | Sort-Object Phase | Format-Table -AutoSize
Write-Host ""
Write-Host "Saved:" -ForegroundColor Green
Write-Host " - $TSV"
Write-Host " - $TSV"
Write-Host " - $MD"
Write-Host " - $JSON"
