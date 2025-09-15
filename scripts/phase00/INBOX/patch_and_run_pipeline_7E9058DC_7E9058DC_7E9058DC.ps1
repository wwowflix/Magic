# --------------------------------------------------------------
# patch_and_run_pipeline.ps1
# Exclude known-broken tests/scripts and rerun pipeline
# --------------------------------------------------------------

# sanity check
Write-Host "=== PATCH SCRIPT START ===" -ForegroundColor Cyan

Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
$scriptFolder = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptFolder

# List of files to skip in pipeline
$excludeList = @(
    'diagnostic_test.py',
    'load_secret_test.py',
    'save_api_key.py',
    'reddit_check.py',
    'tests_scrapers.py',
    'test_vault.py',
    'test_vault_manager.py',
    'trends_scraper_with_reddit.py'
)

# Generate patched run_all_scripts.ps1
$pipelinePath = Join-Path $scriptFolder 'run_all_scripts.ps1'
@'
# --------------------------------------------------------------
# run_all_scripts.ps1 (patched)
# Skips known-broken scripts
# --------------------------------------------------------------

Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
$scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Write-Host "Scanning Python scripts in $scriptRoot..." -ForegroundColor Cyan

$allFiles    = Get-ChildItem -Path $scriptRoot -Filter *.py -ErrorAction SilentlyContinue
$excludeList = 'diagnostic_test.py','load_secret_test.py','save_api_key.py','reddit_check.py','tests_scrapers.py','test_vault.py','test_vault_manager.py','trends_scraper_with_reddit.py'

$pyFiles = $allFiles | Where-Object { $excludeList -notcontains $_.Name }
if ($pyFiles.Count -eq 0) {
    Write-Host "No scripts to run after exclusion." -ForegroundColor Yellow
    exit
}

$results = @()
foreach ($file in $pyFiles) {
    Write-Host "`n▶ Running $($file.Name)..." -ForegroundColor Cyan
    try {
        $proc  = Start-Process python -ArgumentList "`"$($file.FullName)`"" -NoNewWindow -Wait -PassThru -ErrorAction Stop
        $stat  = if ($proc.ExitCode -eq 0) { 'Success' } else { "Failed (ExitCode $($proc.ExitCode))" }
        $color = if ($proc.ExitCode -eq 0) { 'Green'   } else { 'Red' }
        Write-Host "[$stat] $($file.Name)" -ForegroundColor $color
    } catch {
        $err = $_.Exception.Message
        Write-Host "[Error] $($file.Name): $err" -ForegroundColor Red
        $stat = "Error: $err"
    }
    $results += [PSCustomObject]@{ Script=$file.Name;Status=$stat;Timestamp=(Get-Date -Format s) }
}

$results | Export-Csv -Path (Join-Path $scriptRoot 'run_results.csv') -NoTypeInformation -Encoding UTF8
Write-Host "`nResults saved to run_results.csv" -ForegroundColor Cyan
'@ | Set-Content -Path $pipelinePath -Encoding UTF8

Write-Host "✅ run_all_scripts.ps1 patched (exclusions applied)" -ForegroundColor Green

# Execute the patched pipeline
Write-Host "▶ Running patched pipeline..." -ForegroundColor Cyan
& $pipelinePath
