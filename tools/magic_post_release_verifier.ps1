param(
    [string]$Root = (Get-Location).Path
)

$ErrorActionPreference = "Stop"

Write-Host "🔎 MAGIC post-release check (local)..." -ForegroundColor Cyan

# 1) repo clean?
$gitStatus = git status --porcelain
if ($gitStatus) {
    Write-Warning "⚠ Git working tree is NOT clean:"
    $gitStatus
} else {
    Write-Host "✅ Git working tree clean."
}

# 2) workflow must exist + contain artifact upload block
$wfPath = ".github\workflows\tests.yml"
$wfOk = $false
if (-not (Test-Path $wfPath)) {
    Write-Warning "⚠ Workflow $wfPath not found."
} else {
    $wfText = Get-Content $wfPath -Raw
    $needles = @(
        "Upload dashboard artifacts",
        "actions/upload-artifact@v4",
        "path: outputs/reports/",
        "if-no-files-found: warn"
    )
    $missing = @()
    foreach ($n in $needles) {
        if ($wfText -notmatch [regex]::Escape($n)) {
            $missing += $n
        }
    }
    if ($missing.Count -gt 0) {
        Write-Warning "⚠ Workflow found but these lines are missing:"
        $missing | ForEach-Object { "  - $_" }
    } else {
        Write-Host "✅ Workflow has dashboard artifact upload block."
        $wfOk = $true
    }
}

# 3) reports dir present + not empty
$reportsDir = "outputs\reports"
$reportsOk  = $false
if (-not (Test-Path $reportsDir)) {
    Write-Warning "⚠ $reportsDir does NOT exist. CI upload will have nothing."
} else {
    $files = Get-ChildItem $reportsDir -File -ErrorAction SilentlyContinue
    if ($files.Count -eq 0) {
        Write-Warning "⚠ $reportsDir exists but is EMPTY."
    } else {
        Write-Host "✅ $reportsDir exists with $($files.Count) file(s)."
        $reportsOk = $true
    }
}

# 4) venv present
$venvPython = Join-Path $Root "venv\Scripts\python.exe"
if (Test-Path $venvPython) {
    Write-Host "✅ venv python present at $venvPython"
} else {
    Write-Warning "⚠ venv python NOT found at $venvPython"
}

# 5) coverage + snapshot check
$coverageXml = "outputs\reports\coverage.xml"
$releaseSnap = "outputs\reports\release_status_snapshot.txt"

if (Test-Path $coverageXml) {
    $covInfo = Get-Item $coverageXml
    $ageMinutes = (New-TimeSpan -Start $covInfo.LastWriteTime -End (Get-Date)).TotalMinutes
    Write-Host ("✅ coverage.xml found. Age: {0:N1} minutes" -f $ageMinutes)
    if ($ageMinutes -gt 1440) {
        Write-Warning "⚠ coverage.xml older than 1 day – consider re-running tests."
    }
} else {
    Write-Warning "⚠ coverage.xml missing – re-run .\tools\magic_test_runner.ps1"
}

if (-not (Test-Path $releaseSnap)) {
    Write-Warning "⚠ release_status_snapshot.txt missing – run .\tools\magic_quick_status.ps1"
} else {
    $snapInfo = Get-Item $releaseSnap
    Write-Host ("✅ release_status_snapshot.txt found. LastWrite: {0}" -f $snapInfo.LastWriteTime)
}

# 6) smoke pytest
if (Test-Path $venvPython) {
    Write-Host "🧪 Running smoke pytest on tests/status ..." -ForegroundColor Yellow
    try {
        & $venvPython -m pytest -q tests/status --maxfail=1 --disable-warnings
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Smoke pytest PASS (tests/status)."
        } else {
            Write-Warning "⚠ Smoke pytest FAILED with exit code $LASTEXITCODE."
        }
    } catch {
        Write-Warning "⚠ Smoke pytest could not run: $_"
    }
}

# 7) coverage.ini check
$covIni = "coverage.ini"
if (Test-Path $covIni) {
    $covText = Get-Content $covIni -Raw
    if ($covText -match "omit\s*=") {
        Write-Host "✅ coverage.ini present with omit block."
    } else {
        Write-Warning "⚠ coverage.ini present but omit block missing."
    }
} else {
    Write-Warning "⚠ coverage.ini missing."
}

Write-Host "✅ MAGIC post-release check (local) done." -ForegroundColor Green
