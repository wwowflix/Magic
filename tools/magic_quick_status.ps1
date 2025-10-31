# tools\magic_quick_status.ps1
# MAGIC Quick Status (safe version)

$ErrorActionPreference = "Stop"

Write-Host "🧠 MAGIC Quick Status"

# 1) Root
$root = Get-Location
Write-Host "Root: $root"

# 2) Venv check
$venvPy = "E:\MAGIC\venv\Scripts\python.exe"
if (Test-Path $venvPy) {
    Write-Host "Venv: OK ($venvPy)"
} else {
    Write-Warning "Venv: MISSING (expected $venvPy)"
}

# 3) DB check
$dbPath = "E:\MAGIC\outputs\mydata.db"
if (Test-Path $dbPath) {
    Write-Host "Database: OK ($dbPath)"
} else {
    Write-Warning "Database: MISSING ($dbPath)"
}

# 4) Scheduler (SOFT) — THIS IS THE IMPORTANT CHANGE
$taskName = "MAGIC_Trends_Hourly"
$schedMsg = $null
try {
    $null = schtasks /Query /TN $taskName /FO LIST 2>$null
    if ($LASTEXITCODE -eq 0) {
        $schedMsg = "Scheduler: OK ($taskName)"
        Write-Host $schedMsg
    } else {
        $schedMsg = "Scheduler: MISSING or access denied ($taskName)"
        Write-Warning $schedMsg
    }
} catch {
    $schedMsg = "Scheduler: MISSING or access denied ($taskName)"
    Write-Warning $schedMsg
}

# 5) Snapshot writer
$reportsDir = "outputs\reports"
if (-not (Test-Path $reportsDir)) {
    New-Item -ItemType Directory -Force -Path $reportsDir | Out-Null
}

$snapshot = Join-Path $reportsDir "release_status_snapshot.txt"

"Date: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" | Out-File -FilePath $snapshot -Encoding UTF8
"Repo: $(git rev-parse --abbrev-ref HEAD 2>$null)" | Out-File -FilePath $snapshot -Encoding UTF8 -Append

$reportCount = (Get-ChildItem $reportsDir -File -ErrorAction SilentlyContinue).Count
"Reports: $reportCount" | Out-File -FilePath $snapshot -Encoding UTF8 -Append

if ($schedMsg) {
    $schedMsg | Out-File -FilePath $snapshot -Encoding UTF8 -Append
}

Write-Host "✅ Quick status complete."
