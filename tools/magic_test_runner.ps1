param(
    [switch]$Clean
)

Write-Host "🔁 MAGIC Test Runner" -ForegroundColor Cyan

# 1) optional cleanup
if ($Clean) {
    if (Test-Path .\.coverage) {
        Remove-Item -Force .\.coverage
        Write-Host "🧹 removed old .coverage"
    }
}

# 2) run pytest with the safe ignores
python -m pytest -q --maxfail=1 --disable-warnings -p pytest_cov --cov=. --cov-report=xml `
    --ignore=tests/smoke `
    --ignore=tests/test_build_dashboard.py `
    --ignore=tests/test_dashboard_import.py `
    --ignore=tests/test_trends_collector.py

# 3) move coverage if it was created
if (Test-Path .\coverage.xml) {
    Move-Item -Force .\coverage.xml .\outputs\reports\coverage.xml
    Write-Host "✅ coverage.xml -> outputs\reports\coverage.xml"
} else {
    Write-Host "❗ coverage.xml missing – pytest failed or was interrupted."
}

# 4) refresh MAGIC status
if (Test-Path .\tools\magic_status_scan.ps1) {
    .\tools\magic_status_scan.ps1
}
if (Test-Path .\tools\magic_quick_status.ps1) {
    .\tools\magic_quick_status.ps1
}

Write-Host "✅ MAGIC test runner done."
