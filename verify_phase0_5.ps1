# Phase 0–5 verifier
$ErrorActionPreference = "SilentlyContinue"

function New-Row($phase,$step,$check,$ok,$details) {
  [pscustomobject]@{
    Phase   = $phase
    Step    = $step
    Check   = $check
    Status  = if ($ok -eq $true) { "✅ PASS" } elseif ($ok -eq $false) { "❌ FAIL" } else { "⚠ MANUAL" }
    Details = $details
  }
}
function Test-File($path) { Test-Path -LiteralPath $path -PathType Leaf }
function Test-Folder($path) { Test-Path -LiteralPath $path -PathType Container }
function Test-Content($path,$rx) { if (-not (Test-File $path)) { $false } else { Select-String -Path $path -Pattern $rx -SimpleMatch -Quiet } }
function Which($exe) { (Get-Command $exe -ErrorAction SilentlyContinue) -ne $null }
function Git($args) { git $args 2>$null }
function HasGit() { Which git }
function GitRepo() { (HasGit) -and (Test-Path ".git") }
function GitHasRemote() { if (-not (GitRepo)) { $false } else { (Git "remote -v") | Out-String | Select-String -Pattern "origin" -Quiet } }
function TestScheduledTask($name) { (schtasks /Query /TN $name 2>$null) -match $name }

$rows = @()
$rows += New-Row 0 "0.1" "one_time_organizer.py exists" (Test-File "scripts\one_time_organizer.py") "scripts\one_time_organizer.py"
$rows += New-Row 0 "0.2" "RULES dict present in organizer" (Test-Content "scripts\one_time_organizer.py" "RULES =") "looks for 'RULES =' in organizer"
$rows += New-Row 0 "0.3" "venv exists" (Test-Folder "venv\Scripts") "venv\Scripts"
$rows += New-Row 0 "0.4" "post-organizer folders exist" ((Test-Folder "scripts") -and (Test-Folder "outputs\trends") -and (Test-Folder "logs/archive")) "scripts/, outputs/trends/, logs/archive/"
$rows += New-Row 0 "0.5" "assets folder (optional)" $null "assets/ (manual)"

$rows += New-Row 1 "1.1" "Git repo initialized" (GitRepo) ".git folder"
$rows += New-Row 1 "1.2" ".gitignore correct" (Test-File ".gitignore" -and (Select-String ".gitignore" -Pattern "venv/" -Quiet) -and (Select-String ".gitignore" -Pattern ".env" -Quiet) -and (Select-String ".gitignore" -Pattern "__pycache__/" -Quiet)) ".gitignore contains venv/, .env, __pycache__/"
$rows += New-Row 1 "1.4" "Remote origin set" (GitHasRemote) "git remote -v shows origin"

$rows += New-Row 3 "3.1" "docs/naming.md exists" (Test-File "docs\naming.md") "docs/naming.md"
$rows += New-Row 3 "3.3" "scripts/setup_folders.py exists" (Test-File "scripts\setup_folders.py") "ensure_dirs() present?"
$rows += New-Row 3 "3.4" "scripts/config.py exists" (Test-File "scripts\config.py") "config.py with paths"

$rows += New-Row 4 "4.1" "folder_audit.py exists" (Test-File "scripts\folder_audit.py") "audit script present"
$rows += New-Row 4 "4.2" "folder_cleanup.py exists" (Test-File "scripts\folder_cleanup.py") "cleanup script present"
$rows += New-Row 4 "4.3" "start_check.py exists" (Test-File "scripts\start_check.py") "start check present"

$rows += New-Row 5 "5.2" "requirements.txt exists" ((Test-File "requirements.txt") -and ((Get-Item "requirements.txt").Length -gt 0)) "pip freeze > requirements.txt"
$rows += New-Row 5 "5.3" "Bootstrap scripts exist" ((Test-File "setup.ps1") -and (Test-File "setup.sh")) "setup.ps1 & setup.sh"
$rows += New-Row 5 "5.5" "docs/onboarding.md exists" (Test-File "docs\onboarding.md") "onboarding checklist present"

$rows | Sort-Object Phase, Step | Format-Table -AutoSize
