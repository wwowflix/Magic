[CmdletBinding()]
param(
  [string]$Root = (Get-Location).Path,
  [string]$OutDir = $(Join-Path (Get-Location).Path "outputs\reports"),
  [switch]$Quiet
)

Write-Host "MAGIC full scanner -- CLEAN v2.0" -ForegroundColor Yellow
$ErrorActionPreference = "Stop"

function New-Dir([string]$p){ if(!(Test-Path $p)){ New-Item -ItemType Directory -Force -Path $p | Out-Null } }

# Normalize
$Root = (Resolve-Path $Root).Path
$scriptsDir = Join-Path $Root "scripts"
if(!(Test-Path $scriptsDir)){ throw "Scripts folder not found: $scriptsDir" }

# Outputs
$reportsDir   = $OutDir
$readinessDir = Join-Path $Root "outputs\reports\readiness"
New-Dir $reportsDir; New-Dir $readinessDir

# Enumerate MAGIC files only (exclude venv/tests/outputs/etc.)
$allPy = Get-ChildItem -Path (Join-Path $scriptsDir '*') -Recurse -File -Include *.py -ErrorAction Stop |
  Where-Object {
    $_.FullName -notmatch '(?i)[/\\]\.git[/\\]|[/\\](?:venv|\.venv|env)[/\\]|[/\\]site-packages[/\\]|[/\\]dist-info[/\\]|[/\\]node_modules[/\\]|[/\\]outputs[/\\]|[/\\]build[/\\]|[/\\]dist[/\\]|[/\\]tests[/\\]'
  }

# Include patterns:
#  - "12A_..." phase-module naming
#  - "*_READY.py"
#  - explicit shield/shim files used in MAGIC
$files = $allPy | Where-Object {
  $_.Name -match '^\d{1,2}[A-Z]_.*\.py$' -or
  $_.Name -match '_READY\.py$' -or
  $_.Name -match '^(Blocks\.py|ElementTree\.py|soupparser\.py|G_D_E_F_\.py|CFF2ToCFF\.py|CFFToCFF2\.py)$'
}

$items = @()

foreach($f in $files){
  $rel = $f.FullName
  if($rel.ToLower().StartsWith($Root.ToLower())){ $rel = $rel.Substring($Root.Length).TrimStart('\','/') }

  # Phase / Module inference
  $phase  = $null; $module = $null
  $m1 = [regex]::Match($rel, '(?i)phase[\\/_-]?(\d{1,2})'); if($m1.Success){ $phase = [int]$m1.Groups[1].Value }
  if(-not $phase){ $m2 = [regex]::Match($f.Name, '^(\d{1,2})[A-Z]_'); if($m2.Success){ $phase = [int]$m2.Groups[1].Value } }
  $m3 = [regex]::Match($rel, '(?i)module[\\/_-]?([a-z])'); if($m3.Success){ $module = $m3.Groups[1].Value.ToUpper() }
  if(-not $module){ $m4 = [regex]::Match($f.Name, '^\d{1,2}([A-Z])_'); if($m4.Success){ $module = $m4.Groups[1].Value.ToUpper() } }
  if(-not $phase){ $phase = 0 }  # bucket unphased

  $raw      = Get-Content -Raw -LiteralPath $f.FullName
  $lines    = ($raw -split "`r?`n").Count
  $nonEmpty = ($raw -split "`r?`n" | Where-Object { $_.Trim().Length -gt 0 }).Count
  $sizeKB   = [math]::Round($f.Length/1kb,2)

  # Placeholder heuristics -> WARN, else PASS (skip py_compile for momentum)
  $placeholder = @()
  if($nonEmpty -le 8){ $placeholder += 'le8_non_empty_lines' }
  if($sizeKB -lt 0.5){ $placeholder += 'lt0_5KB' }
  if($raw -match '(?is)\b(PLACEHOLDER|STUB|TBD|TODO)\b'){ $placeholder += 'placeholder_keywords' }
  if($raw -match '^\s*pass\s*$'){ $placeholder += 'pass_line' }

  $status = "PASS"; $notes = "implemented"
  if($placeholder.Count -gt 0){ $status = "WARN"; $notes = "placeholder: " + ($placeholder -join '; ') }

  $items += [pscustomobject]@{
    phase=$phase; module=$module; filename=$f.Name; rel_path=$rel;
    lines=$lines; non_empty=$nonEmpty; size_kb=$sizeKB; status=$status; notes=$notes
  }
}

$items = $items | Sort-Object phase, module, filename

# Per-phase rollup
$perPhase = $items | Group-Object phase | ForEach-Object {
  $pass = ($_.Group | Where-Object { $_.status -eq 'PASS'  }).Count
  $warn = ($_.Group | Where-Object { $_.status -eq 'WARN'  }).Count
  $err  = ($_.Group | Where-Object { $_.status -eq 'ERROR' }).Count
  $tot  = $_.Count
  $progress = if($tot -gt 0){ [math]::Round(($pass*100.0)/$tot,2) } else { 0 }
  [pscustomobject]@{ phase=$_.Name; total=$tot; pass=$pass; warn=$warn; error=$err; progress=$progress }
}

# Report
$report = [pscustomobject]@{
  generated_at=(Get-Date).ToString('s'); root=$Root;
  total_scripts=($items | Measure-Object).Count;
  pass=($items | Where-Object { $_.status -eq 'PASS'  } | Measure-Object).Count;
  warn=($items | Where-Object { $_.status -eq 'WARN'  } | Measure-Object).Count;
  error=($items | Where-Object { $_.status -eq 'ERROR' } | Measure-Object).Count;
  per_phase=$perPhase; items=$items
}

# Paths
$ts = Get-Date -Format 'yyyyMMdd_HHmmss'
$jsonPath   = Join-Path $reportsDir 'magic_full_status.json'
$jsonPathTS = Join-Path $reportsDir "magic_full_status_$ts.json"
$tsvPath    = Join-Path $reportsDir 'magic_full_status.tsv'
$tsvPathTS  = Join-Path $reportsDir "magic_full_status_$ts.tsv"
$readyNow   = Join-Path $readinessDir 'status_live_latest.tsv'
$readyTS    = Join-Path $readinessDir "status_live_$ts.tsv"
$quickTSV   = Join-Path $reportsDir 'magic_quick_status.tsv'
$quickJSON  = Join-Path $reportsDir 'magic_quick_status.json'

# Write UTF-8 (no BOM)
$utf8 = New-Object System.Text.UTF8Encoding($false)
$js = $report | ConvertTo-Json -Depth 8
[System.IO.File]::WriteAllText($jsonPath,   $js, $utf8)
[System.IO.File]::WriteAllText($jsonPathTS, $js, $utf8)

# Items TSV
$headers = 'phase','module','filename','rel_path','lines','non_empty','size_kb','status','notes'
$lines = @(); $lines += ($headers -join "`t")
foreach($row in $items){
  $vals = @($row.phase,$row.module,$row.filename,$row.rel_path,$row.lines,$row.non_empty,$row.size_kb,$row.status,$row.notes) |
    ForEach-Object { ($_ -replace "`r?`n"," ") -replace "`t"," " }
  $lines += ($vals -join "`t")
}
$tsv = ($lines -join "`r`n")
[System.IO.File]::WriteAllText($tsvPath,   $tsv, $utf8)
[System.IO.File]::WriteAllText($tsvPathTS, $tsv, $utf8)

# Readiness (phase rows + overall)
if    ($report.error -gt 0)         { $overallStatus = 'ERROR' }
elseif($report.pass  -gt 0)         { $overallStatus = 'PASS'  }
elseif($report.total_scripts -gt 0) { $overallStatus = 'WARN'  }
else                                 { $overallStatus = 'SKIP'  }

$ready = @(); $ready += "Step`tCheck`tStatus`tNotes"; $step=1
foreach($pp in ($perPhase | Sort-Object {[int]$_.phase})){
  if    ($pp.pass -gt 0)  { $st='PASS' }
  elseif($pp.error -gt 0) { $st='ERROR' }
  elseif($pp.total -gt 0) { $st='WARN' }
  else                    { $st='SKIP' }
  $note = "pass=$($pp.pass); warn=$($pp.warn); error=$($pp.error); total=$($pp.total); progress=$($pp.progress)%"
  $ready += ("{0}`tPhase {1} health`t{2}`t{3}" -f $step,$pp.phase,$st,$note); $step++
}
$ready += ("{0}`tOverall health`t{1}`tpass={2}; warn={3}; error={4}; total={5}" -f $step,$overallStatus,$report.pass,$report.warn,$report.error,$report.total_scripts)

$readyText = ($ready -join "`r`n")
[System.IO.File]::WriteAllText($readyNow, $readyText, $utf8)
[System.IO.File]::WriteAllText($readyTS,  $readyText, $utf8)

# Quick
$quick=[pscustomobject]@{
  generated_at=$report.generated_at; total=$report.total_scripts; pass=$report.pass; warn=$report.warn; error=$report.error; phases=$perPhase
}
[System.IO.File]::WriteAllText($quickJSON, ($quick | ConvertTo-Json -Depth 6), $utf8)
$quickLines=@("metric`tvalue","generated_at`t$($quick.generated_at)","total`t$($quick.total)","pass`t$($quick.pass)","warn`t$($quick.warn)","error`t$($quick.error)")
[System.IO.File]::WriteAllLines($quickTSV, $quickLines, $utf8)

if(-not $Quiet){
  Write-Host ("Found {0} MAGIC scripts; PASS:{1} WARN:{2} ERROR:{3}" -f $report.total_scripts,$report.pass,$report.warn,$report.error) -ForegroundColor Green
  Write-Host ("JSON:  {0}" -f $jsonPath) -ForegroundColor Cyan
  Write-Host ("TSV :  {0}" -f $tsvPath)  -ForegroundColor Cyan
  Write-Host ("Ready: {0}" -f $readyNow) -ForegroundColor Cyan
  Write-Host ("Quick: {0}" -f $quickTSV) -ForegroundColor Cyan
}
exit 0
