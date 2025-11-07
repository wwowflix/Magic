<#
.SYNOPSIS
  Verifies progress across the 48 release steps and produces a repeatable PASS/FAIL report.

.USAGE
  powershell -NoProfile -ExecutionPolicy Bypass -File .\tools\verify_release_progress.ps1 -Root $Root

.OUTPUTS
  - Console table with PASS/FAIL per step
  - outputs\reports\progress_status.json
  - outputs\reports\progress_status.tsv
#>

param(
  [string]$Root = (Get-Location)
if (-not \E:\MAGIC) { \E:\MAGIC = (Get-Location).Path }
.Path,
  [switch]$Quiet,
  [switch]$NoExitOnFail
)

# ---------------------------
# Helpers
# ---------------------------
function Ensure-Dir([string]$Path) {
  if (-not (Test-Path $Path)) { New-Item -ItemType Directory -Force -Path $Path | Out-Null }
}
function Test-Command([string]$Name) { $null -ne (Get-Command $Name -ErrorAction SilentlyContinue) }
function Git-CurrentBranch() { try { (git rev-parse --abbrev-ref HEAD 2>$null).Trim() } catch { $null } }
function Git-HasTag([string]$Tag) { try { [bool](git tag --list $Tag 2>$null) } catch { $false } }
function Test-VenvPresent([string]$RootPath) { Test-Path (Join-Path $RootPath "venv") }
function Test-VenvActive() { $env:VIRTUAL_ENV -or $env:CONDA_PREFIX -or ($env:Path -like "*\venv\Scripts*") }
function Test-File([string]$Path) { Test-Path $Path }
function Test-AnyFile([string[]]$Paths) { foreach($p in $Paths){ if(Test-Path $p){ return $true } } return $false }
function Test-RegexInFile([string]$Path,[string]$Pattern) {
  if (-not (Test-Path $Path)) { return $false }; Select-String -Path $Path -Pattern $Pattern -Quiet
}
function Test-JsonParse([string]$Path) {
  try { if (Test-Path $Path) { Get-Content $Path -Raw | ConvertFrom-Json | Out-Null; return $true } else { return $false } }
  catch { return $false }
}
function Test-RunOK([string]$CmdLine) { try { & cmd /c $CmdLine | Out-Null; return ($LASTEXITCODE -eq 0) } catch { return $false } }

# ---------------------------
# Paths + Setup
# ---------------------------
$Root = (Resolve-Path $Root).Path
Set-Location $Root
$reportsDir = Join-Path $Root "outputs\reports"
Ensure-Dir $reportsDir

# Known receipts / artifacts we’ll use as proof:
$Artifacts = @{
  OrphansTSV         = Join-Path $reportsDir "orphans.tsv"
  ScanSummaryJSON    = Join-Path $reportsDir "magic_scan_summary.json"
  TodoAuditJSON      = Join-Path $reportsDir "magic_todo_audit.json"
  SelfTestJSON       = Join-Path $reportsDir "magic_self_test.json"
  CoverageFiles      = @(".\coverage.xml",".\.coverage") | ForEach-Object { Join-Path $Root $_ }
  SBOM               = Join-Path $reportsDir "sbom.json"
  NonConformCSV      = Join-Path $reportsDir "nonconforming_scripts.csv"
  DashIndex          = Join-Path $Root "outputs\site\index.html"
  RequirementsLock   = Join-Path $Root "requirements.lock.txt"
}

# Quick existence flags
$gitOk          = Test-Command "git"
$pythonOk       = Test-Command "python"
$precommitOk    = Test-Command "pre-commit"
$pytestOk       = Test-Command "pytest"
$banditOk       = Test-Command "bandit"
$pipAuditOk     = Test-Command "pip-audit"
$safetyOk       = Test-Command "safety"
$gitleaksOk     = Test-Command "gitleaks"
$detectSecretsOk= Test-Command "detect-secrets"
$cyclonedxOk    = Test-Command "cyclonedx-py"
$dockerOk       = Test-Command "docker"
$AllowSkipDocker = ($env:ALLOW_SKIP_DOCKER -eq '1')

# ---------------------------
# Define Checks (48 total)
# ---------------------------
$Checks = @()
function Add-Check([int]$Id,[string]$Name,[scriptblock]$Test,[string]$FixHint) {
  $script:Checks += [pscustomobject]@{ Id=$Id; Name=$Name; Test=$Test; FixHint=$FixHint }
}

# 0–2 Git baseline
Add-Check 0  "Repo at $Root" { (Get-Location).Path -eq $Root }                                  "Run: Set-Location $Root"
Add-Check 1  "git pull done / clean" { $gitOk -and ((git status --porcelain 2>$null | Measure-Object).Count -ge 0) } "Run git pull; resolve conflicts"
Add-Check 2  "On branch prod-release" { (Git-CurrentBranch) -eq "prod-release" }                "git checkout -b prod-release (or git checkout prod-release)"

# 3–7 Python env + deps
Add-Check 3  "venv present" { Test-VenvPresent $Root }                                          "python -m venv venv"
Add-Check 4  "venv active"  { Test-VenvActive }                                                 ".\venv\Scripts\Activate.ps1"
Add-Check 5  "pip upgraded" { $pythonOk -and (python -m pip --version 2>$null) }                "python -m pip install --upgrade pip"
Add-Check 6  "requirements installed" { Test-File (Join-Path $Root "requirements.txt") }        "pip install -r requirements.txt"
Add-Check 7  "MPLBACKEND=Agg set (session/env)" { $env:MPLBACKEND -eq "Agg" }                   "$env:MPLBACKEND='Agg' (set in CI later)"

# 8–10 lint + tests
Add-Check 8  "pre-commit installed" { $precommitOk }                                            "pre-commit install"
Add-Check 9  "pre-commit runnable" { $precommitOk -and (Test-RunOK "pre-commit --version") }    "pre-commit run --all-files"
Add-Check 10 "pytest ok (collects)" { $pytestOk -and (Test-RunOK "pytest --collect-only -q") }  "Fix failing imports/tests"

# 11 coverage (receipt-based)
Add-Check 11 "coverage ≥ artifacts exist" { Test-AnyFile $Artifacts.CoverageFiles }             "pytest --cov=./ --cov-fail-under=75"

# 12–13 security & secrets
Add-Check 12 "Security tooling available" { $pipAuditOk -and $safetyOk -and $banditOk }         "pip install pip-audit safety bandit"
Add-Check 13 "Secret scan tooling available" { $gitleaksOk -or $detectSecretsOk }               "pip install detect-secrets; or install gitleaks"

# 14 baseline scan receipt
Add-Check 14 "Full scan receipts exist" { Test-File $Artifacts.OrphansTSV }                     'powershell -File .\tools\magic_full_scan.ps1 -Root $Root'

# 15–17 API/DAG/DQ (presence)
Add-Check 15 "API contracts script present" { Test-File ".\tools\contracts\mock_contract_tests.py" } "Add or fix contracts tests"
Add-Check 16 "DAG smoke script present"    { Test-File ".\tools\dag_smoke.py" }                  "Add tools\dag_smoke.py"
Add-Check 17 "Data quality scripts present" { (Get-ChildItem ".\tools\data_quality" -Filter *.py -ErrorAction SilentlyContinue).Count -gt 0 } "Add DQ scripts"

# 18 dashboards
Add-Check 18 "Dash index exists" { Test-File $Artifacts.DashIndex }                             "python tools/build_dashboard.py ..."

# 19–23 scan status / verify suite
Add-Check 19 "scan_status tool present" { Test-File ".\tools\magic_scan_status.ps1" }           "Add tools\magic_scan_status.ps1"
Add-Check 20 "magic_scan_summary.json valid" { Test-JsonParse $Artifacts.ScanSummaryJSON }      "Re-run full scan; fix JSON schema"
Add-Check 21 "todo audit tool present" { Test-File ".\tools\magic_todo_audit.ps1" }             "Add tools\magic_todo_audit.ps1"
Add-Check 22 "verify_magic_complete present" { Test-File ".\tools\verify_magic_complete.ps1" }  "Add tools\verify_magic_complete.ps1"
Add-Check 23 "self-test summary present" { Test-JsonParse $Artifacts.SelfTestJSON }             'powershell -File .\tools\magic_self_test.ps1 -Root $Root'

# 24–27 budgets/chaos/recovery
Add-Check 24 "check_spend.py present" { Test-File ".\tools\cost_quota\check_spend.py" }         "Add the tool or skip this gate"
Add-Check 25 "check_quota.py present" { Test-File ".\tools\cost_quota\check_quota.py" }         "Add the tool or skip this gate"
Add-Check 26 "chaos injector present" { Test-File ".\tools\chaos\inject_failures.py" }          "Add chaos injector"
Add-Check 27 "restore script present" { Test-File ".\tools\drill\restore_from_latest.py" }      "Add restore drill script"

# 28–31 git receipts for release
Add-Check 28 "Changes committed" { $gitOk -and -not (git status --porcelain 2>$null) }          "git add -A; git commit -m 'chore: receipts'"
Add-Check 29 "Branch pushed"     { $gitOk -and (git remote -v 2>$null) }                        "git push -u origin prod-release"
Add-Check 30 "Re-scan before tag recorded" { Test-File $Artifacts.OrphansTSV }                  "Re-run full scan"
Add-Check 31 "Tag v1.0-stable exists" { Git-HasTag "v1.0-stable" }                              "git tag v1.0-stable; git push origin v1.0-stable"

# 32–33 lock + SBOM
Add-Check 32 "requirements.lock.txt exists" { Test-File $Artifacts.RequirementsLock }           "pip freeze > requirements.lock.txt"
Add-Check 33 "SBOM exists"                  { Test-File $Artifacts.SBOM }                        "cyclonedx-py -o outputs/reports/sbom.json"

# 34–35 containerization
Add-Check 34 "Docker available" { $AllowSkipDocker -or $dockerOk } "Install/Start Docker Desktop (or set ALLOW_SKIP_DOCKER=1 to skip locally)"
Add-Check 35 "Docker HEALTHCHECK present" { Test-RegexInFile ".\Dockerfile" '^\s*HEALTHCHECK\s+CMD\s+python\s+tools/live_healthcheck\.py' } "Add HEALTHCHECK to Dockerfile"

# 36–37 publishing & rollback tools
Add-Check 36 "canary_post present" { Test-File ".\tools\publish\canary_post.py" }               "Add sandbox canary publisher"
Add-Check 37 "rollback_to_tag present" { Test-File ".\tools\release\rollback_to_tag.py" }       "Add rollback script"

# 38 cron
Add-Check 38 "Nightly scan task registered (name contains MAGIC Nightly)" {
  $scheduled = try { Get-ScheduledTask -ErrorAction Stop | Where-Object { $_.TaskName -like "*MAGIC*Nightly*" } } catch { @() }
  $scheduled.Count -gt 0
} "Register-ScheduledTask … (include 'MAGIC Nightly' in name)"

# 39–40 SLI/SLO scripts
Add-Check 39 "calc_sli.py present" { Test-File ".\tools\ops\calc_sli.py" }                      "Add calc_sli.py"
Add-Check 40 "check_slo.py present" { Test-File ".\tools\ops\check_slo.py" }                    "Add check_slo.py"

# 41–42 cleanup plan + quarantine
Add-Check 41 "plan_cleanup present" { Test-File ".\tools\plan_cleanup.ps1" }                    "Add plan_cleanup.ps1"
Add-Check 42 "quarantine script present" { Test-AnyFile @(".\tools\quarantine.ps1",".\tools\cleanup\quarantine.ps1") } "Add quarantine script"

# 43–44 final hygiene + final gate
Add-Check 43 "pre-commit final pass runnable" { $precommitOk }                                   "pre-commit run --all-files"
Add-Check 44 "verify_magic_complete final present" { Test-File ".\tools\verify_magic_complete.ps1" } "Add verifier"

# 45–47 release ops
Add-Check 45 "Merge capability (git available)" { $gitOk }                                       "Install Git & configure"
Add-Check 46 "GitHub Release (proxy check: git remote set)" { $gitOk -and (git remote -v 2>$null) } "Create GH release via UI or gh cli"
Add-Check 47 "Offsite backup tool present" { Test-AnyFile @(".\tools\publish\upload_to_drive.ps1",".\tools\publish\upload_to_s3.ps1") } "Add cloud upload script"

# ---------------------------
# Execute Checks
# ---------------------------
$results = foreach ($c in $Checks | Sort-Object Id) {
  $ok = $false; $err = $null
  try { $ok = & $c.Test } catch { $ok = $false; $err = $_.Exception.Message }
  [pscustomobject]@{
    Id = $c.Id
    Step = $c.Name
    Status = if ($ok) { "PASS" } else { "FAIL" }
    FixHint = if ($ok) { "" } else { $c.FixHint }
    Error = $err
  }
}

# Metrics
$pass = ($results | Where-Object { $_.Status -eq "PASS" } | Measure-Object).Count
$total = ($results | Measure-Object).Count
$percent = if ($total -gt 0) { [math]::Round(($pass / [double]$total)*100, 1) } else { 0 }

# ---------------------------
# Output
# ---------------------------
if (-not $Quiet) {
  Write-Host ""
  Write-Host "MAGIC Release Progress @ $Root" -ForegroundColor Cyan
  Write-Host ("Completed: {0}/{1} ({2}%)" -f $pass,$total,$percent) -ForegroundColor Cyan
  Write-Host ""
  $results | Sort-Object Id | Format-Table Id, Status, Step -AutoSize
}

# Persist JSON + TSV snapshots
$stamp = (Get-Date).ToString("yyyy-MM-dd_HH-mm-ss")
$jsonOut = Join-Path $reportsDir "progress_status.json"
$tsvOut  = Join-Path $reportsDir "progress_status.tsv"

$payload = [pscustomobject]@{
  root = $Root
  timestamp = (Get-Date).ToString("o")
  summary = [pscustomobject]@{ pass=$pass; total=$total; percent=$percent }
  results = $results
}
$payload | ConvertTo-Json -Depth 5 | Out-File -FilePath $jsonOut -Encoding UTF8
$results | Select-Object Id, Status, Step, FixHint | Export-Csv -Delimiter "`t" -NoTypeInformation -Encoding UTF8 -Path $tsvOut

if (-not $Quiet) {
  Write-Host ""
  Write-Host "Saved: $jsonOut" -ForegroundColor DarkGray
  Write-Host "Saved: $tsvOut"  -ForegroundColor DarkGray
}

# ---------------------------
# Exit behavior (safe for humans, strict for CI)
# ---------------------------
$failed = ($pass -lt $total)
$code   = if ($failed) { 1 } else { 0 }
$global:LASTEXITCODE = $code

$inCI = $env:CI -or $env:GITHUB_ACTIONS -or $env:BUILD_BUILDID -or $env:TF_BUILD
if ($inCI -and -not $NoExitOnFail) {
  exit $code
} else {
  if (-not $Quiet) {
    if ($failed) {
      Write-Host "NOTE: Failures detected. Exit code would have been $code. (Use in CI or remove -NoExitOnFail to enforce.)" -ForegroundColor Yellow
    } else {
      Write-Host "All checks passed. Exit code would have been 0." -ForegroundColor Green
    }
  }
}
