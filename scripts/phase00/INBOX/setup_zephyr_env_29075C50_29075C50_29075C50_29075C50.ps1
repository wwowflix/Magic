<#
.SYNOPSIS
  Automate Zephyr project setup, patching, renaming, and testing.
.DESCRIPTION
  - Renames all .ps scripts to .ps1
  - Sets execution policy for current session
  - Patches Python scripts for BOM-safe JSON loading and UTF-8 stdout
  - Generates the test harness script (test_scripts_status.ps1)
  - Ensures PRAW is installed
  - Executes the test harness
.EXAMPLE
  PS> .\setup_zephyr_env.ps1
#>

# Determine and switch to script directory
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

# 1) Rename all .ps → .ps1
Write-Host "Renaming .ps → .ps1 scripts..." -ForegroundColor Cyan
Get-ChildItem -Filter *.ps | Rename-Item -NewName { $_.BaseName + ".ps1" } -Force

# 2) Allow script execution for this session
Write-Host "Setting execution policy..." -ForegroundColor Cyan
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force

# 3) Patch Python scripts for BOM-safe JSON & UTF-8 output
$pyFiles = @("trends_scraper.py","tiktok_xhr_scraper.py")
foreach ($file in $pyFiles) {
    if (Test-Path $file) {
        Write-Host "Patching $file..." -ForegroundColor Cyan
        Copy-Item $file "${file}.bak" -Force
        $content = Get-Content -Raw -Path $file
        # BOM-safe JSON loading
        $content = $content -replace 'with\s+open\(([^,\)]+)\)', 'with open($1, "r", encoding="utf-8-sig")'
        # Add UTF-8 stdout header if missing
        if ($content -notmatch 'sys\.stdout\.reconfigure') {
            $header = @"
import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

"@
            $content = $header + $content
        }
        Set-Content -Path $file -Value $content -Encoding UTF8
    }
}

# 4) Generate test harness script
$testHarness = @'
# test_scripts_status.ps1

# Define test cases
$tests = @(
    @{Name='Google Trends';       File='trends_scraper.py';    Args='--source google'},
    @{Name='YouTube Autocomplete';File='trends_scraper.py';    Args='--source youtube'},
    @{Name='Orchestrator';        File='orchestrator.py';      Args='--dry-run'},
    @{Name='TikTok XHR Scraper';  File='tiktok_xhr_scraper.py';Args=''}
)

Write-Host "`n🚀 Running Zephyr script tests..." -ForegroundColor Cyan
Push-Location $ScriptDir
$results = @()
foreach ($t in $tests) {
    $path = Join-Path $ScriptDir $t.File
    if (-not (Test-Path $path)) {
        $results += [PSCustomObject]@{ Script = $t.Name; Status = 'Not Found'; Command = '' }
        continue
    }
    $cmd = if ($t.Args) { "python `"$path`" $($t.Args)" } else { "python `"$path`"" }
    Write-Host "▶ Testing $($t.Name): $cmd" -ForegroundColor DarkGray
    Invoke-Expression $cmd | Out-Null
    $status = if ($LASTEXITCODE -eq 0) { 'Working' } else { 'Failed' }
    $results += [PSCustomObject]@{ Script = $t.Name; Status = $status; Command = $cmd }
}
Pop-Location

Write-Host "`nTest Results:" -ForegroundColor Cyan
$results | Format-Table -AutoSize
Write-Host "`n✅ All tests complete." -ForegroundColor Green
'@
Set-Content -Path '.\test_scripts_status.ps1' -Value $testHarness -Encoding UTF8
Write-Host "Created test_scripts_status.ps1." -ForegroundColor Green

# 5) Ensure PRAW is installed
Write-Host "Checking for PRAW..." -ForegroundColor Cyan
pip show praw > $null 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "Installing PRAW..." -ForegroundColor Yellow
    pip install praw
} else {
    Write-Host "PRAW already installed." -ForegroundColor Green
}

# 6) Run the test harness
Write-Host "`nExecuting test harness..." -ForegroundColor Cyan
& .\test_scripts_status.ps1

Write-Host "`nSetup and testing complete!" -ForegroundColor Green
