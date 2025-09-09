param([string]$Root="D:\MAGIC",[int]$Timeout=8)
$ErrorActionPreference='Stop'
Set-Location $Root

function Pass($n,$i=""){ "{0,-18} PASS  {1}" -f $n,$i }
function Fail($n,$i=""){ "{0,-18} FAIL  {1}" -f $n,$i; $script:failed=$true }

# Prefer venv python; fallback to PATH python
$pyPref = Join-Path $Root "venv\Scripts\python.exe"
if (Test-Path $pyPref) { $py = $pyPref } else { $py = (Get-Command python).Source }

# Exclusions + bad suffixes
$ExcludedRegex='\\(inbox|samples|playground|backups|outputs|quarantine|\.git|\.pytest_cache|\.mypy_cache|\.ruff_cache|__pycache__|venv|\.venv)\\'
$BadSuffixRegex='(\.BAK(_BOM)?$|\.BAK_BOM$|\.bak$|\.tmp$)'

# Manifests
$manifestEntr = Join-Path $Root "prod_entrypoints.txt"
$manifestGlobs= Join-Path $Root "prod_compile_globs.txt"

# ---- Expand compile globs (PS5-friendly); return *_READY.py only ----
function Get-CompileSet {
  $out = @()
  if (Test-Path $manifestGlobs) {
    $globs = Get-Content $manifestGlobs -ErrorAction SilentlyContinue | Where-Object { $_ }
    foreach($g in $globs){
      if (Test-Path $g) {
        $p = (Resolve-Path $g).Path
        if ((Get-Item $p).PSIsContainer) {
          $out += Get-ChildItem $p -Recurse -File -Filter "*_READY.py" -ErrorAction SilentlyContinue
        } else {
          if ($p -like "*_READY.py") { $out += Get-Item $p -ErrorAction SilentlyContinue }
        }
      } elseif ($g -match '^\w:') {
        $dir = Split-Path $g
        $pat = Split-Path $g -Leaf
        if (Test-Path $dir) {
          $out += Get-ChildItem $dir -Recurse -File -Include $pat -ErrorAction SilentlyContinue
        }
      }
    }
  }
  $out = $out | Where-Object {
    $_ -and ($_.FullName -notmatch $ExcludedRegex) -and
    ($_.Name -like "*_READY.py") -and
    ($_.FullName -notmatch $BadSuffixRegex)
  } | Sort-Object FullName -Unique
  return $out
}

# ---- Entrypoints strictly from manifest; trim quotes; no autodiscovery ----
function Get-Entrypoints {
  if (Test-Path $manifestEntr) {
    return @(Get-Content $manifestEntr -ErrorAction SilentlyContinue |
      Where-Object { $_ } |
      ForEach-Object {
        $p = $_.Trim() -replace '^[\"'']|[\"'']$',''
        if (Test-Path $p) { Get-Item $p }
      } |
      Where-Object { $_ -and ($_.FullName -notmatch $ExcludedRegex) -and ($_.Name -like "*.py") } |
      Sort-Object FullName -Unique)
  }
  return @()
}

# 1) Placeholders over compile set
$compileSet = Get-CompileSet
$ph=@(
  $compileSet | ForEach-Object {
    $t=Get-Content -Raw -LiteralPath $_.FullName -ErrorAction SilentlyContinue
    if($null -ne $t -and $t.Trim() -match '^\s*(""" Placeholder.*"""|#\s*placeholder|#\s*TODO|\.\.\.)\s*$'){ $_ }
  })
if($ph.Count -eq 0){ Pass "placeholders" "none" } else { Fail "placeholders" "$($ph.Count) files" }

# 2) Compile set (direct invocation; reliable $LASTEXITCODE)
$compileIssues=@()
foreach($p in $compileSet){
  $out = & $py -m py_compile $p.FullName 2>&1
  $code = $LASTEXITCODE
  if($code -ne 0){
    $msg = ($out | Select-Object -Last 5) -join " "
    if(-not $msg){ $msg="py_compile failed" }
    $compileIssues += "compile: $($p.FullName) -> $msg"
  }
}
if($compileIssues.Count -eq 0){ Pass "compile_set" "0 issues across $($compileSet.Count) files" }
else { Fail "compile_set" "$($compileIssues.Count) issues across $($compileSet.Count) files"; ($compileIssues | Select-Object -First 10) | ForEach-Object { "  -> $_" } }

# 3) Run entrypoints (direct invocation; use venv python if available)
$entrypoints = Get-Entrypoints
if($entrypoints.Count -eq 0){
  Pass "run_entrypoints" "skipped (no entrypoints listed)"
} else {
  $runIssues=@()
  foreach($p in $entrypoints){
    $out = & $py $p.FullName 2>&1
    $code = $LASTEXITCODE
    if($code -ne 0){
      $msg = ($out | Select-Object -Last 10) -join " "
      if(-not $msg){ $msg = "nonzero exit" }
      $runIssues += "runtime: $($p.FullName) -> $msg"
    }
  }
  if($runIssues.Count -eq 0){ Pass "run_entrypoints" "0 issues across $($entrypoints.Count) files" }
  else { Fail "run_entrypoints" "$($runIssues.Count) issues across $($entrypoints.Count) files"; ($runIssues | Select-Object -First 10) | ForEach-Object { "  -> $_" } }
}

# 4) CI workflow presence
if(Test-Path ".github\workflows\ci.yml"){ Pass "ci_workflow" ".github\workflows\ci.yml" } else { Fail "ci_workflow" "missing .github\workflows\ci.yml" }

if($script:failed){ exit 1 } else { exit 0 }
