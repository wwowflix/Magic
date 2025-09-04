$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"

function To-Bool($v){
  if($null -eq $v){ return $false }
  if($v -is [bool]){ return $v }
  if($v -is [int]) { return $v -ne 0 }
  $s = ([string]$v).Trim().ToLower()
  return $s -in @('true','1','yes')
}
function Pass($m){ Write-Host ("  ? {0}" -f $m) -ForegroundColor Green }
function Fail($m){ Write-Host ("  ? {0}" -f $m) -ForegroundColor Red; $script:FAILED += 1 }
function Info($m){ Write-Host ("  ? {0}" -f $m) -ForegroundColor DarkCyan }

function Load-LatestReport {
  $reports = Get-ChildItem "outputs\reports\week_status_report_*.tsv" -ErrorAction SilentlyContinue |
             Sort-Object LastWriteTime -Desc
  if(-not $reports){ throw "No TSV found under outputs\reports" }
  $latest = $reports[0]

  $rows = Import-Csv -Delimiter "`t" -Path $latest.FullName | Where-Object {
    $_.Week -match '^\s*\d+\s*$'
  } | ForEach-Object {
    [pscustomobject]@{
      Week   = ($_.Week   -replace '"','').Trim()
      Step   = ($_.Step   -replace '"','').Trim()
      Goal   = ($_.Goal   -replace '"','')
      Result = ($_.Result -replace '"','')
      Why    = ($(if($_.PSObject.Properties.Name -contains 'Why'){ $_.Why } else { '' }))
    }
  }

  if(-not $rows){ throw "Report $($latest.Name) parsed empty" }
  ,@($latest, $rows)
}

function Make-Lookup($rows){
  $t = @{}
  foreach($r in $rows){
    $k = ("{0}|{1}" -f $r.Week,$r.Step)
    $t[$k] = To-Bool $r.Result
  }
  $t
}

Write-Host ""
Write-Host "== Weeks Completion Proof ==" -ForegroundColor Cyan

$FAILED = 0
$tuple = Load-LatestReport
$latest = $tuple[0]
$rows   = $tuple[1]
$lookup = Make-Lookup $rows

$CRITICAL = @{
  '1'=@('1.1','1.2'); '2'=@('2.1'); '3'=@('3.4'); '4'=@('4.1'); '5'=@('5.2');
  '6'=@('6.3'); '7'=@('7.3'); '8'=@('8.1'); '9'=@('9.1');
  '10'=@('10.1'); '11'=@('11.3'); '12'=@('12.2')
}

Write-Host ("Report: {0}" -f $latest.Name) -ForegroundColor DarkGray

# [1] Critical Steps present & passing
Write-Host "`n[1] Critical Steps" -ForegroundColor Yellow
$missing = @()
$failed  = @()
foreach($kv in $CRITICAL.GetEnumerator() | Sort-Object Name){
  $w = $kv.Key
  foreach($s in $kv.Value){
    $key = ("{0}|{1}" -f $w,$s)
    if(-not $lookup.ContainsKey($key)){ $missing += $key }
    elseif(-not $lookup[$key]){ $failed += $key }
  }
}
if($missing.Count -gt 0){ Fail ("Missing from report: {0}" -f ($missing -join ", ")) } else { Pass "All critical steps present" }
if($failed.Count  -gt 0){ Fail ("Critical steps not True: {0}" -f ($failed -join ", ")) } else { Pass "All critical steps are True" }

# [2] Per-week thresholds
Write-Host "`n[2] Per-Week Thresholds (crit pass OR >=60%)" -ForegroundColor Yellow
$grouped = $rows | Group-Object Week
$badWeeks = @()
foreach($g in $grouped){
  $w = [string]$g.Name
  $items = $g.Group
  $passed = ($items | Where-Object { To-Bool $_.Result }).Count
  $pct = [math]::Round(100 * $passed / [math]::Max(1,$items.Count))
  $crit = $CRITICAL[$w]
  $critPass = $false
  if($crit){
    $arr = @()
    foreach($step in $crit){
      $k = ("{0}|{1}" -f $w,$step)
      if($lookup.ContainsKey($k)){ $arr += $lookup[$k] } else { $arr += $false }
    }
    $critPass = ($arr -notcontains $false)
  }
  if(-not ($critPass -or $pct -ge 60)){
    $badWeeks += [pscustomobject]@{Week=$w;Pct=$pct;Crit=$critPass}
  }
}
if($badWeeks.Count -gt 0){
  $descItems = @()
  foreach($b in $badWeeks){ $descItems += ("{0} (pct={1}, crit={2})" -f $b.Week,$b.Pct,$b.Crit) }
  Fail ("Weeks failing threshold: {0}" -f ($descItems -join "; "))
}else{
  Pass "All weeks meet thresholds"
}

# [3] CI Checks & PR Triggers
Write-Host "`n[3] CI Checks & PR Triggers" -ForegroundColor Yellow
$ci = ".github\workflows\ci.yml"
if(Test-Path $ci){
  $y = Get-Content $ci -Raw -Encoding UTF8
  if($y -match "pull_request"){ Pass "ci.yml runs on pull_request" } else { Fail "ci.yml missing pull_request trigger" }
  if($y -match "(?m)^\s*name:\s*tests\s*$"){ Pass "tests job declared" } else { Fail "tests job missing in ci.yml" }
  if($y -match "(?m)^\s*name:\s*mypy\s*$"){  Pass "mypy job declared" }  else { Fail "mypy job missing in ci.yml" }
}else{
  Fail "Missing .github/workflows/ci.yml"
}

# [4] Release Notes & Artifact Workflows
Write-Host "`n[4] Release Notes & Artifact Workflows" -ForegroundColor Yellow
$notes = "docs\releases\RELEASE_NOTES_v1.0-stable.md"
if(Test-Path $notes){ Pass ("Release notes present: {0}" -f $notes) } else { Fail ("Release notes missing: {0}" -f $notes) }

$rn = ".github\workflows\release_notes.yml"
$pa = ".github\workflows\publish_artifacts.yml"
if(Test-Path $rn){ Pass "Workflow present: release_notes.yml" } else { Fail "Missing workflow: release_notes.yml" }
if(Test-Path $pa){ Pass "Workflow present: publish_artifacts.yml" } else { Fail "Missing workflow: publish_artifacts.yml" }

# [5] Version Tag (optional)
Write-Host "`n[5] Version Tag (optional)" -ForegroundColor Yellow
$allowMissing = $env:ALLOW_MISSING_TAG -eq '1'
try{
  $null = (Get-Command git -ErrorAction Stop).Source
  $tags = (git tag) -split "`r?`n"
  if($tags -contains "v1.0-stable"){
    Pass "Git tag v1.0-stable found"
  }elseif($allowMissing){
    Info "Tag v1.0-stable not found locally (ALLOW_MISSING_TAG=1)"
  }else{
    Fail "Git tag v1.0-stable not found (set ALLOW_MISSING_TAG=1 to allow)"
  }
}catch{
  Info "git not available; skipping tag check"
}

# [6] Metrics & Cleanup
Write-Host "`n[6] Metrics & Cleanup" -ForegroundColor Yellow
$metrics = "outputs\metrics\metrics.json"
if(Test-Path $metrics){ Pass ("Metrics present: {0}" -f $metrics) } else { Fail "Missing metrics file: outputs\metrics\metrics.json (Week 8.1)" }
$cleanup = ".github\workflows\cleanup_logs.yml"
if(Test-Path $cleanup){ Pass "Cleanup workflow present (Week 9.3)" } else { Fail "Missing cleanup_logs.yml (Week 9.3)" }

# [7] Runner Features
Write-Host "`n[7] Runner Features (Parallel & AI remediation)" -ForegroundColor Yellow
$runner = "self_healing_runner_v5.py"
if(Test-Path $runner){
  $rtxt = Get-Content $runner -Raw -Encoding UTF8
  if($rtxt -match "concurrent\.futures\.ProcessPoolExecutor|multiprocessing"){ Pass "Parallel execution detected (Week 6.3)" } else { Fail "Parallel execution not detected in v5 runner (Week 6.3)" }
  if($rtxt -match "apply_remediation"){ Pass "apply_remediation present (Weeks 3.x/11.x)" } else { Fail "apply_remediation missing" }
  if($rtxt -match "apply_remediation_ai" -or (Test-Path "tools\auto_patcher.py")){ Pass "AI remediation or auto_patcher present (Week 11)" } else { Fail "AI remediation/auto_patcher not detected (Week 11)" }
}else{
  Fail ("Missing {0}" -f $runner)
}

# [8] Week 5.2 artifact
Write-Host "`n[8] Week 5.2 Concrete Output" -ForegroundColor Yellow
$w52 = "scripts\phase11\module_B\reports\summary_module_b.tsv"
if(Test-Path $w52){ Pass ("Found Week 5.2 summary: {0}" -f $w52) } else { Fail ("Week 5.2 summary not found: {0}" -f $w52) }

# Summary
if($FAILED -gt 0){
  Write-Host ("`nFAILED ({0} checks failed)" -f $FAILED) -ForegroundColor Red
  exit 1
}else{
  Write-Host "`nALL GOOD ?" -ForegroundColor Green
  exit 0
}
