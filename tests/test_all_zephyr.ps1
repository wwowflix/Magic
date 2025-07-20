# test_all_zephyr.ps1

# 1. Patch trends_scraper.py for BOM-safe JSON loading
$pyFile = "D:\MAGIC\scripts\trends_scraper.py"
$backup = "$pyFile.bak"

if (-not (Test-Path $backup)) {
    Copy-Item $pyFile $backup -Force
    Write-Host "Backed up trends_scraper.py to trends_scraper.py.bak"
}

# Insert encoding="utf-8-sig" into every with open(...) call
(Get-Content $pyFile) | ForEach-Object {
    if ($_ -match 'with open\(') {
        $_ -replace 'with open\(([^,]+)\)', 'with open($1, "r", encoding="utf-8-sig")'
    }
    else {
        $_
    }
} | Set-Content $pyFile -Encoding utf8

Write-Host "Patched trends_scraper.py for BOM-safe JSON loading."

# 2. Define the test commands
$tests = @(
    @{ Name = 'Z.9 CSV schema (--help)';   Cmd = 'python trends_scraper.py --help' },
    @{ Name = 'Z.7/Z.8 Orchestrator';      Cmd = 'python orchestrator.py --dry-run' },
    @{ Name = 'Z.1 Google Trends';         Cmd = 'python trends_scraper.py --source google' },
    @{ Name = 'Z.4 YouTube Autocomplete';  Cmd = 'python trends_scraper.py --source youtube' },
    @{ Name = 'Z.2 TikTok XHR Scraper';    Cmd = 'python tiktok_xhr_scraper.py' }
)

Write-Host ""
Write-Host "Running all Zephyr tests..." -ForegroundColor Cyan

# 3. Execute each test
Push-Location "D:\MAGIC\scripts"

foreach ($t in $tests) {
    Write-Host ""
    Write-Host "▶ $($t.Name)" -NoNewline
    Write-Host "  $($t.Cmd)" -ForegroundColor DarkGray

    Invoke-Expression $t.Cmd

    if ($LASTEXITCODE -eq 0) {
        Write-Host " ✓ Passed" -ForegroundColor Green
    }
    else {
        Write-Host " ✗ FAILED (exit code $LASTEXITCODE)" -ForegroundColor Red
    }
}

Pop-Location

Write-Host ""
Write-Host "All done!" -ForegroundColor Cyan
