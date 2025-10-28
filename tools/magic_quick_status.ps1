param(
    [string]$Root = "E:\MAGIC"
)

Write-Host "🧙 MAGIC Quick Status" -ForegroundColor Cyan
Write-Host "Root: $Root"

# ===== VENV CHECK =====
$venvPy = "$Root\venv\Scripts\python.exe"
if (Test-Path $venvPy) {
    Write-Host "Venv: OK ($venvPy)"
} else {
    Write-Host "Venv: MISSING ($venvPy)" -ForegroundColor Yellow
}

# ===== DB CHECK =====
$db = "$Root\outputs\mydata.db"
if (Test-Path $db) {
    Write-Host "Database: OK ($db)"
} else {
    Write-Host "Database: MISSING ($db)" -ForegroundColor Yellow
}

# ===== TASK CHECK =====
$taskName = "MAGIC_Trends_Hourly"
schtasks /Query /TN $taskName /FO LIST > $null 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "Scheduler: OK (task exists)"
} else {
    Write-Host "Scheduler: MISSING ($taskName)" -ForegroundColor Yellow
}

Write-Host "✅ Quick status complete."
