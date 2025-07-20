# ==========================
# test_dashboard_suite.ps1
# ==========================

function Test-PyScript {
    param (
        [string] $scriptName
    )
    if (Test-Path ".\$scriptName") {
        Write-Host "`n→ Running $scriptName..." -ForegroundColor Cyan
        python ".\$scriptName"
    } else {
        Write-Host "⚠️  NOT FOUND: $scriptName" -ForegroundColor Yellow
    }
}

# Run your Python test scripts:

Test-PyScript "charts.py"
Test-PyScript "trend_predictor.py"
Test-PyScript "report_generator.py"

Write-Host "`n=== ✅ DASHBOARD SUITE TEST HARNESS COMPLETE ===" -ForegroundColor Green
