# --------------------------------------------------------------
Write-Host "`nResults saved to run_results.csv" -ForegroundColor Cyan
$results | Export-Csv -Path (Join-Path $scriptRoot 'run_results.csv') -NoTypeInformation -Encoding UTF8
$excludeList = @(
)
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
    Write-Host "`nâ–¶ Running $($file.Name)..." -ForegroundColor Cyan
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
