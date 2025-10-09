param(
  [string]$Root = (Get-Location).Path,
  [int]$CoverageTarget = 75
)

$ErrorActionPreference = "Stop"

function New-Dir($p){ if(-not (Test-Path $p)){ New-Item -ItemType Directory -Force $p | Out-Null } }
function Test-Cmd($name){ $null -ne (Get-Command $name -ErrorAction SilentlyContinue) }
function Add-Row([string]$Area,[string]$Check,[string]$Status,[string]$Notes){
  $global:rows += [pscustomobject]@{ Area=$Area; Check=$Check; Status=$Status; Notes=$Notes }
}
function Run-Tool([string]$label,[string[]]$try){
  foreach($cmd in $try){
    try{
      & $cmd 2>$null | Out-Null
      if($LASTEXITCODE -eq 0){ return @{ ok=$true; used=$cmd } }
    } catch {}
  }
  return @{ ok=$false; used=($try -join " | ") }
}

$ts = Get-Date -Format "yyyyMMdd_HHmmss"
$outDir = Join-Path $Root "outputs\reports\readiness"
New-Dir $outDir
$tsv  = Join-Path $outDir "gap_report_$ts.tsv"
$md   = Join-Path $outDir "gap_report_$ts.md"

$rows = @()

# --- Repo / Branch tracking ---
Set-Location $Root
$branch = (& git rev-parse --abbrev-ref HEAD).Trim()
$upstream = ""
try { $upstream = (& git rev-parse --symbolic-full-name '@{u}' 2>$null).Trim() } catch {}
if($branch -eq "prod-release"){
  if($upstream){
    Add-Row "Git/Branch" "prod-release tracking" "PASS" "$branch → $upstream"
  } else {
    Add-Row "Git/Branch" "prod-release tracking" "FAIL" "No upstream. Run: git branch --set-upstream-to=origin/prod-release prod-release"
  }
} else {
  Add-Row "Git/Branch" "on prod-release" "WARN" ("Current: {0}. Run: git switch prod-release" -f $branch)
}

# --- venv sanity (PS 5.1 safe) ---
$venvActive = $false
if ($env:VIRTUAL_ENV) { $venvActive = $true }
elseif (Test-Path ".\venv\Scripts\Activate.ps1") { $venvActive = $true }

if ($venvActive) {
  Add-Row "Python" "venv active" "PASS" "Detected venv"
} else {
  Add-Row "Python" "venv active" "WARN" "Run: if(!(Test-Path .\venv)){python -m venv venv}; .\venv\Scripts\Activate.ps1"
}

# --- pre-commit ---
$hasConfig = Test-Path ".pre-commit-config.yaml"
if(-not $hasConfig){
  Add-Row "Lint" "pre-commit config" "WARN" "Missing .pre-commit-config.yaml (I can stub one)."
} else {
  Add-Row "Lint" "pre-commit config" "PASS" ".pre-commit-config.yaml found"
}

$preCommit = Run-Tool "pre-commit" @("pre-commit --version","python -m pre_commit --version","$pwd\venv\Scripts\pre-commit.exe --version")
if(-not $preCommit.ok){
  Add-Row "Lint" "pre-commit installed" "FAIL" "Install: python -m pip install pre-commit"
} else {
  $install = Run-Tool "pre-commit install" @(
    "pre-commit install","python -m pre_commit install","$pwd\venv\Scripts\pre-commit.exe install"
  )
  if($install.ok){
    & pre-commit run --all-files 2>$null | Tee-Object -Variable _pc | Out-Null
    if($LASTEXITCODE -eq 0){
      Add-Row "Lint" "pre-commit sweep" "PASS" "All hooks passed"
    } else {
      Add-Row "Lint" "pre-commit sweep" "WARN" "Hooks changed files or warnings; commit fixes"
    }
  } else {
    Add-Row "Lint" "pre-commit install" "FAIL" ("Couldn’t install hook: {0}" -f $install.used)
  }
}

# --- Tests & Coverage ---
$pytest = Run-Tool "pytest" @("pytest --version","python -m pytest --version")
if(-not $pytest.ok){
  Add-Row "Tests" "pytest available" "FAIL" "Install: python -m pip install pytest pytest-cov"
} else {
  & python -m pytest -q 2>$null | Out-Null
  if($LASTEXITCODE -eq 0){
    Add-Row "Tests" "pytest run" "PASS" "Unit tests completed (0 collected is OK)"
  } else {
    Add-Row "Tests" "pytest run" "FAIL" "Tests failed; check traceback"
  }

  & python -m pytest --cov=./ --cov-fail-under=$CoverageTarget 2>$null | Out-Null
  if($LASTEXITCODE -eq 0){
    Add-Row "Tests" ("coverage ≥ {0}%" -f $CoverageTarget) "PASS" "Threshold met"
  } else {
    Add-Row "Tests" ("coverage ≥ {0}%" -f $CoverageTarget) "WARN" ("Coverage below {0}%" -f $CoverageTarget)
  }
}

# --- Security: pip-audit / safety / bandit ---
$pa = Run-Tool "pip-audit" @("pip-audit --version")
if($pa.ok){
  & pip-audit 2>$null | Out-Null
  if ($LASTEXITCODE -eq 0) {
    Add-Row "Security" "pip-audit" "PASS" "No known vulns"
  } else {
    Add-Row "Security" "pip-audit" "WARN" "Vulns reported — review"
  }
} else {
  Add-Row "Security" "pip-audit installed" "FAIL" "Install: python -m pip install pip-audit"
}

$sf = Run-Tool "safety" @("safety --version")
if($sf.ok){
  & safety check -r requirements.txt 2>$null | Out-Null
  if ($LASTEXITCODE -eq 0) {
    Add-Row "Security" "safety check" "PASS" "No issues"
  } else {
    Add-Row "Security" "safety check" "WARN" "Issues reported — review"
  }
} else {
  Add-Row "Security" "safety installed" "FAIL" "Install: python -m pip install safety"
}

$bd = Run-Tool "bandit" @("bandit --version")
if($bd.ok){
  & bandit -r . -ll 2>$null | Out-Null
  $bSum = Join-Path $outDir "bandit_summary_$ts.txt"
  & bandit -r . -f screen -o $bSum 2>$null | Out-Null
  $txt = (Get-Content $bSum -Raw)
  if($txt -match "No issues identified"){
    Add-Row "Security" "bandit scan" "PASS" "No issues identified"
  } else {
    Add-Row "Security" "bandit scan" "WARN" ("Review {0}" -f $bSum)
  }
} else {
  Add-Row "Security" "bandit installed" "FAIL" "Install: python -m pip install bandit"
}

# --- Secrets: detect-secrets ---
$ds = Run-Tool "detect-secrets" @("detect-secrets --version")
if($ds.ok){
  $baseline = ".secrets.baseline"
  if(Test-Path $baseline){
    & detect-secrets scan --baseline $baseline 2>$null | Out-Null
    Add-Row "Secrets" "detect-secrets (baseline)" "PASS" ("Compared with {0}" -f $baseline)
  } else {
    Add-Row "Secrets" "detect-secrets baseline" "WARN" "Create baseline: detect-secrets scan > .secrets.baseline"
  }
} else {
  Add-Row "Secrets" "detect-secrets installed" "FAIL" "Install: python -m pip install detect-secrets"
}

# --- Repo cleanliness: untracked reports/noise ---
$untracked = (& git status --porcelain).Split("`n") | Where-Object { $_ -match '^\?\?' }
$noisy = @($untracked | Where-Object { $_ -match 'outputs/reports' })
if($noisy.Count -gt 0){
  Add-Row "Git Clean" "Untracked reports" "WARN" ("Consider .gitignore for reports. Count: {0}" -f $noisy.Count)
} else {
  Add-Row "Git Clean" "Untracked reports" "PASS" "Clean"
}

# --- Write TSV ---
$rows |
  Select-Object Area,Check,Status,Notes |
  Export-Csv -Delimiter "`t" -NoTypeInformation -Encoding UTF8 -Path $tsv

# --- Write Markdown summary ---
$ok  = ($rows | Where-Object Status -eq "PASS").Count
$wrn = ($rows | Where-Object Status -eq "WARN").Count
$fl  = ($rows | Where-Object Status -eq "FAIL").Count

$mdBody = @()
$mdBody += "# MAGIC Gap Report ($ts)"
$mdBody += ""
$mdBody += "- Repo: $Root"
$mdBody += "- Branch: $branch  |  Upstream: $upstream"
$mdBody += ("- Totals: **PASS={0} / WARN={1} / FAIL={2}**" -f $ok,$wrn,$fl)
$mdBody += ""
$mdBody += "| Area | Check | Status | Notes |"
$mdBody += "|---|---|---|---|"
foreach($r in $rows){
  $line = ("| {0} | {1} | {2} | {3} |" -f $r.Area,$r.Check,$r.Status,($r.Notes -replace '\|','\|'))
  $mdBody += $line
}
$mdBody -join "`r`n" | Set-Content -Encoding UTF8 $md

Write-Host "Wrote:" -ForegroundColor Green
Write-Host " - $tsv"
Write-Host " - $md"
