# fix_and_test_zephyr.ps1

# 1) Backup & patch JSON loads to use utf-8-sig
$pyFiles = @(
  "D:\MAGIC\scripts\trends_scraper.py",
  "D:\MAGIC\scripts\tiktok_xhr_scraper.py"
)

foreach ($pyFile in $pyFiles) {
  $bak = "$pyFile.bak"
  if (-not (Test-Path $bak)) {
    Copy-Item $pyFile $bak -Force
    Write-Host "Backed up $($pyFile | Split-Path -Leaf) to $($bak | Split-Path -Leaf)"
  }

  (Get-Content $pyFile) |
    ForEach-Object {
      if ($_ -match 'with\s+open\(') {
        # keep only the first argument, add mode and utf-8-sig
        $_ -replace 'open\(\s*([^)]+?)(?:,[^)]+)?\)',
                    'open($1, "r", encoding="utf-8-sig")'
      }
      else {
        $_
      }
    } |
    Set-Content $pyFile -Encoding utf8

  Write-Host "Patched $($pyFile | Split-Path -Leaf) for BOM-safe JSON loading."
}

# 2) Ensure Chrome drivers quit cleanly (silence WinError 6)
foreach ($pyFile in $pyFiles) {
  if (-not (Select-String -Path $pyFile -Pattern 'driver\.quit')) {
    Add-Content $pyFile ''
    Add-Content $pyFile '# cleanup Chrome driver handle'
    Add-Content $pyFile 'try:'
    Add-Content $pyFile '    driver.quit()'
    Add-Content $pyFile 'except:'
    Add-Content $pyFile '    pass'
    Write-Host "Appended driver.quit() cleanup to $($pyFile | Split-Path -Leaf)."
  }
}

# 3) Define end-to-end tests
$tests = @(
  @{ Name = 'Z.9 Schema (--help)';     Cmd = 'python trends_scraper.py --help' },
  @{ Name = 'Z.7/Z.8 Orchestrator';     Cmd = 'python orchestrator.py --dry-run' },
  @{ Name = 'Z.1 Google Trends';        Cmd = 'python trends_scraper.py --source google' },
  @{ Name = 'Z.4 YouTube';              Cmd = 'python trends_scraper.py --source youtube' },
  @{ Name = 'Z.2 TikTok';               Cmd = 'python tiktok_xhr_scraper.py' }
)

Write-Host ""
Write-Host "Running all Zephyr tests..." -ForegroundColor Cyan

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
