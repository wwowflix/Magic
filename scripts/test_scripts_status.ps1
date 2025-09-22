# test_scripts_status.ps1

# Define test cases
$tests = @(
    @{Name='Google Trends';       File='trends_scraper.py';    Args='--source google'},
    @{Name='YouTube Autocomplete';File='trends_scraper.py';    Args='--source youtube'},
    @{Name='Orchestrator';        File='orchestrator.py';      Args='--dry-run'},
    @{Name='TikTok XHR Scraper';  File='tiktok_xhr_scraper.py';Args=''}
)

Write-Host "`nðŸš€ Running Zephyr script tests..." -ForegroundColor Cyan
Push-Location $ScriptDir
$results = @()
foreach ($t in $tests) {
    $path = Join-Path $ScriptDir $t.File
    if (-not (Test-Path $path)) {
        $results += [PSCustomObject]@{ Script = $t.Name; Status = 'Not Found'; Command = '' }
        continue
    }
    $cmd = if ($t.Args) { "python `"$path`" $($t.Args)" } else { "python `"$path`"" }
    Write-Host "â–¶ Testing $($t.Name): $cmd" -ForegroundColor DarkGray
    Invoke-Expression $cmd | Out-Null
    $status = if ($LASTEXITCODE -eq 0) { 'Working' } else { 'Failed' }
    $results += [PSCustomObject]@{ Script = $t.Name; Status = $status; Command = $cmd }
}
Pop-Location

Write-Host "`nTest Results:" -ForegroundColor Cyan
$results | Format-Table -AutoSize
Write-Host "`nâœ… All tests complete." -ForegroundColor Green
