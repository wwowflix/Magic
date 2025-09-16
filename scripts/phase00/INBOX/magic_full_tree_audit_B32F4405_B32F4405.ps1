#requires -Version 5.1
param(
  [string]$Root = "D:\MAGIC",
  [int]$LargeMB = 200,                 # flag large files
  [int]$OldDays = 120,                 # flag files older than N days
  [int]$HashMaxMB = 1024               # avoid hashing ultra-huge files if you want
)

if (-not (Test-Path $Root)) { Write-Error "Root path not found: $Root"; exit 1 }
$RootPath  = (Resolve-Path $Root).Path
$ReportDir = Join-Path $RootPath "outputs\reports"
New-Item -ItemType Directory -Force -Path $ReportDir | Out-Null

$now = Get-Date
$largeBytes = $LargeMB * 1MB
$oldThreshold = $now.AddDays(-$OldDays)

# --- 0) Define rules / expectations ---
$IgnoreDirs = @("venv","node_modules",".git",".pytest_cache","__pycache__",".mypy_cache",".ruff_cache",".tox","dist","build",".idea",".vscode")
$MustHaveDirs = @(
  "scripts","scripts\phase02","scripts\phase03","scripts\phase05","scripts\phase06","scripts\phase08",
  "scripts\phase09","scripts\phase10","scripts\phase11","scripts\phase12","scripts\phase13","scripts\phase14",
  "scripts\phase15","scripts\phase16","scripts\phase17","scripts\phase18",
  "config","docs","outputs","outputs\reports","outputs\logs","assets","tools"
)
$MustHaveFiles = @(
  "README.md","requirements.txt",".env",
  "docs\naming_conventions.md",
  "tools\magic_full_audit.ps1" # previous script (ok if missing, just a check)
)

# Script naming convention for MAGIC slots:
#   NN[A-Z]_<something>[_READY].py   (e.g., 11A_api_key_leak_checker_READY.py)
$PhaseModuleRegex = '^(?<phase>\d{2})(?<mod>[A-Z])_.*?(\.py)$'
$ReadySuffixRegex = '.*_READY\.py$'

# --- 1) Crawl everything (files + dirs) ---
Write-Host "[*] Crawling full tree under $RootPath ..."
$all = Get-ChildItem -LiteralPath $RootPath -Recurse -Force -ErrorAction SilentlyContinue

# Filter “effective” items (honor ignores)
function Is-Ignored {
  param([string]$FullName)
  foreach($p in $IgnoreDirs){
    if ($FullName -match [regex]::Escape("\$p\".Replace("\\","\\"))) { return $true }
    if ($FullName -match ("\\{0}($|\\)" -f [regex]::Escape($p))) { return $true }
  }
  return $false
}

$allDirs = $all | Where-Object { $_.PSIsContainer -and -not (Is-Ignored $_.FullName) }
$allFiles = $all | Where-Object { -not $_.PSIsContainer -and -not (Is-Ignored $_.FullName) }

# --- 2) Build inventory ---
$inv = $allFiles | ForEach-Object {
  $rel = $_.FullName.Substring($RootPath.Length).TrimStart('\','/')
  $isReady = ($_.Name -match $ReadySuffixRegex)
  $pm = [regex]::Match($_.Name, $PhaseModuleRegex)
  $phase = if ($pm.Success) { [int]$pm.Groups['phase'].Value } else { $null }
  $mod   = if ($pm.Success) { $pm.Groups['mod'].Value } else { $null }

  # Hash only if smaller than $HashMaxMB to keep things fast
  $hash = $null
  if ($_.Length -le ($HashMaxMB * 1MB)) {
    try { $hash = (Get-FileHash -Algorithm SHA256 -LiteralPath $_.FullName -ErrorAction Stop).Hash } catch { $hash = $null }
  }

  [pscustomobject]@{
    rel          = $rel
    name         = $_.Name
    ext          = $_.Extension.ToLowerInvariant()
    dir          = (Split-Path $rel -Parent)
    size_bytes   = $_.Length
    size_mb      = [math]::Round($_.Length/1MB,2)
    created      = $_.CreationTime
    modified     = $_.LastWriteTime
    age_days     = [int]($now - $_.LastWriteTime).TotalDays
    phase        = $phase
    module       = $mod
    is_ready     = $isReady
    is_py        = ($_.Extension -match '^\.(py|ps1|psm1)$')
    is_large     = ($_.Length -ge $largeBytes)
    is_old       = ($_.LastWriteTime -lt $oldThreshold)
    sha256       = $hash
  }
}

# --- 3) Structure checks ---
$missingDirs = @()
foreach($d in $MustHaveDirs){
  $p = Join-Path $RootPath $d
  if (-not (Test-Path $p -PathType Container)) { $missingDirs += $d }
}
$missingFiles = @()
foreach($f in $MustHaveFiles){
  $p = Join-Path $RootPath $f
  if (-not (Test-Path $p -PathType Leaf)) { $missingFiles += $f }
}

# Empty directories
$emptyDirs = $allDirs | Where-Object {
  -not (Get-ChildItem -LiteralPath $_.FullName -Force -ErrorAction SilentlyContinue | Where-Object { -not $_.PSIsContainer })
} | ForEach-Object { $_.FullName.Substring($RootPath.Length).TrimStart('\','/') }

# Orphan files (don’t match Phase/Module pattern & also not known infra files)
$InfraWhitelist = @(
  "README.md","requirements.txt",".env",".gitignore","Dockerfile",".dockerignore",
  "pyproject.toml","poetry.lock","Pipfile","Pipfile.lock",
  "setup.cfg","ruff.toml",".flake8","mypy.ini",".editorconfig",
  "CHANGELOG.md","LICENSE","CODEOWNERS"
)
$orphans = $inv | Where-Object {
  $isPM = $_.phase -ne $null -and $_.module -ne $null
  -not $isPM -and -not ($InfraWhitelist -contains $_.name)
}

# Phase/Module slot status (00–18 with A–Z)
$Phases  = 0..18
$Modules = [char[]]([int][char]'A'..[int][char]'Z')

function Slot-Status {
  param([int]$phase,[string]$module)
  $hits = $inv | Where-Object { $_.phase -eq $phase -and $_.module -eq $module -and $_.ext -eq ".py" }
  if (-not $hits -or $hits.Count -eq 0) { return ,@("❌ Missing", @()) }
  $ready = $hits | Where-Object { $_.is_ready } | Select-Object -First 1
  if ($ready) { return ,@("✅ Ready", ($hits.rel)) } else { return ,@("🔄 Placeholder", ($hits.rel)) }
}

$slotResults = New-Object System.Collections.Generic.List[object]
$totalSlots = ($Phases.Count * $Modules.Count)
$idx = 0
foreach($p in $Phases){
  foreach($m in $Modules){
    $idx++; $pct = [int](($idx/$totalSlots)*100)
    Write-Progress -Activity "Phase/Module readiness scoring" -Status "Phase $p Module $m ($pct%)" -PercentComplete $pct
    $status,$files = Slot-Status -phase $p -module $m
    $slotResults.Add([pscustomobject]@{ phase=$p; module=$m; status=$status; files=($files|Sort-Object) })
  }
}

# --- 4) Analytics / summaries ---
# Top folders by size
$sizeByDir = $inv | Group-Object dir | ForEach-Object {
  [pscustomobject]@{
    dir  = if ($_.Name) { $_.Name } else { "." }
    files= $_.Group.Count
    mb   = [math]::Round( ($_.Group | Measure-Object -Property size_bytes -Sum).Sum / 1MB, 2)
  }
} | Sort-Object mb -Descending

# Extension breakdown
$byExt = $inv | Group-Object ext | ForEach-Object {
  [pscustomobject]@{
    ext  = if ($_.Name) {$_.Name} else { "(no ext)" }
    files= $_.Count
    mb   = [math]::Round( ($_.Group | Measure-Object -Property size_bytes -Sum).Sum / 1MB, 2)
  }
} | Sort-Object mb -Descending

# Largest files
$largest = $inv | Sort-Object size_bytes -Descending | Select-Object -First 100

# Old files
$oldFiles = $inv | Where-Object {$_.is_old} | Sort-Object modified | Select-Object -First 200

# Duplicates by hash
$dupes = $inv | Where-Object {$_.sha256} | Group-Object sha256 | Where-Object {$_.Count -gt 1} |
  ForEach-Object {
    [pscustomobject]@{
      sha256 = $_.Name
      count  = $_.Count
      files  = ($_.Group.rel -join '; ')
      total_mb = [math]::Round( ($_.Group | Measure-Object -Property size_bytes -Sum).Sum / 1MB, 2)
    }
  } | Sort-Object -Property @{Expression="count";Descending=$true}, @{Expression="total_mb";Descending=$true}

# --- 5) Save reports ---
$writeCsv = {
  param($data,$path)
  if ($null -eq $data) { return }
  $dir = Split-Path $path -Parent
  New-Item -ItemType Directory -Force -Path $dir | Out-Null
  $data | Export-Csv -NoTypeInformation -Delimiter "`t" -Encoding UTF8 -Path $path
}

$writeJson = {
  param($data,$path)
  if ($null -eq $data) { return }
  $data | ConvertTo-Json -Depth 8 | Out-File -Encoding UTF8 $path
}

$invTsv     = Join-Path $ReportDir "inventory_full.tsv"
$invJson    = Join-Path $ReportDir "inventory_full.json"
& $writeCsv $inv $invTsv
& $writeJson $inv $invJson

$orphTsv    = Join-Path $ReportDir "orphans.tsv"
$orphJson   = Join-Path $ReportDir "orphans.json"
& $writeCsv $orphans $orphTsv
& $writeJson $orphans $orphJson

$missDirTsv = Join-Path $ReportDir "missing_dirs.tsv"
$missDirJson= Join-Path $ReportDir "missing_dirs.json"
& $writeCsv ($missingDirs | ForEach-Object{[pscustomobject]@{path=$_}}) $missDirTsv
& $writeJson $missingDirs $missDirJson

$missFileTsv= Join-Path $ReportDir "missing_files.tsv"
$missFileJson=Join-Path $ReportDir "missing_files.json"
& $writeCsv ($missingFiles | ForEach-Object{[pscustomobject]@{path=$_}}) $missFileTsv
& $writeJson $missingFiles $missFileJson

$emptyDirTsv= Join-Path $ReportDir "empty_dirs.tsv"
$emptyDirJson=Join-Path $ReportDir "empty_dirs.json"
& $writeCsv ($emptyDirs | ForEach-Object{[pscustomobject]@{path=$_}}) $emptyDirTsv
& $writeJson $emptyDirs $emptyDirJson

$sizeDirTsv = Join-Path $ReportDir "size_by_dir.tsv"
$sizeDirJson= Join-Path $ReportDir "size_by_dir.json"
& $writeCsv $sizeByDir $sizeDirTsv
& $writeJson $sizeByDir $sizeDirJson

$extTsv     = Join-Path $ReportDir "ext_breakdown.tsv"
$extJson    = Join-Path $ReportDir "ext_breakdown.json"
& $writeCsv $byExt $extTsv
& $writeJson $byExt $extJson

$largeTsv   = Join-Path $ReportDir "largest_files.tsv"
$largeJson  = Join-Path $ReportDir "largest_files.json"
& $writeCsv $largest $largeTsv
& $writeJson $largest $largeJson

$oldTsv     = Join-Path $ReportDir "old_files.tsv"
$oldJson    = Join-Path $ReportDir "old_files.json"
& $writeCsv $oldFiles $oldTsv
& $writeJson $oldFiles $oldJson

$dupeTsv    = Join-Path $ReportDir "duplicate_files.tsv"
$dupeJson   = Join-Path $ReportDir "duplicate_files.json"
& $writeCsv $dupes $dupeTsv
& $writeJson $dupes $dupeJson

$slotsTsv   = Join-Path $ReportDir "phase_module_readiness.tsv"
$slotsJson  = Join-Path $ReportDir "phase_module_readiness.json"
& $writeCsv ($slotResults | Select-Object phase,module,status,@{n='files';e={($_.files -join ';')}}) $slotsTsv
& $writeJson $slotResults $slotsJson

# Per-phase scorecard
$score = $slotResults | Group-Object phase | ForEach-Object {
  $grp = $_.Group
  [pscustomobject]@{
    phase        = [int]$_.Name
    total        = $grp.Count
    ready        = ($grp | Where-Object {$_.status -like "✅*"}).Count
    placeholder  = ($grp | Where-Object {$_.status -like "🔄*"}).Count
    missing      = ($grp | Where-Object {$_.status -like "❌*"}).Count
    readinessPct = [math]::Round( ( ($grp | Where-Object {$_.status -like "✅*"}).Count / $grp.Count )*100, 1)
  }
} | Sort-Object phase

$scoreTsv  = Join-Path $ReportDir "phase_scorecard.tsv"
$scoreJson = Join-Path $ReportDir "phase_scorecard.json"
& $writeCsv $score $scoreTsv
& $writeJson $score $scoreJson

# --- 6) Console summary ---
$totFiles = $inv.Count
$totDirs  = $allDirs.Count
$readyCt  = ($slotResults | Where-Object {$_.status -like "✅*"}).Count
$phCt     = $slotResults.Count

Write-Host "`n=== MAGIC — FULL FOLDER AUDIT ===" -ForegroundColor Cyan
Write-Host ("Root: {0}" -f $RootPath)
Write-Host ("Dirs: {0} | Files: {1}" -f $totDirs,$totFiles)
Write-Host ("Large (≥{0}MB): {1}" -f $LargeMB, ($inv | ? {$_.is_large}).Count)
Write-Host ("Old (>{0} days): {1}" -f $OldDays, ($inv | ? {$_.is_old}).Count)
Write-Host ("Empty dirs: {0}" -f $emptyDirs.Count)
Write-Host ("Orphan files (no phase/module & not infra): {0}" -f $orphans.Count)
Write-Host ("Phase/Module slots ready: {0}/{1}" -f $readyCt,$phCt)
Write-Host ""
Write-Host "[Reports]" -ForegroundColor Yellow
@(
  "inventory_full.tsv / .json",
  "orphans.tsv / .json",
  "missing_dirs.tsv / .json",
  "missing_files.tsv / .json",
  "empty_dirs.tsv / .json",
  "size_by_dir.tsv / .json",
  "ext_breakdown.tsv / .json",
  "largest_files.tsv / .json",
  "old_files.tsv / .json",
  "duplicate_files.tsv / .json",
  "phase_module_readiness.tsv / .json",
  "phase_scorecard.tsv / .json"
) | ForEach-Object { Write-Host " - $ReportDir\$_" }
