param(
    [string]$Python = "python"
)

# ---------------------------------------------------------------------------
# Locate repo root relative to this script (tools/ops  tools  repo root)
# ---------------------------------------------------------------------------
$scriptDir = $PSScriptRoot
$toolsDir  = Split-Path $scriptDir -Parent
$repoRoot  = Split-Path $toolsDir -Parent

Set-Location $repoRoot

$manifestPath = Join-Path $repoRoot "config\flow_manifest_week1.json"
$summaryPath  = Join-Path $repoRoot "config\report_week1_summary.json"

if (-not (Test-Path $manifestPath)) {
    Write-Host "Week-1: manifest not found at $manifestPath" -ForegroundColor Red
    exit 1
}

# ---------------------------------------------------------------------------
# Load manifest
# ---------------------------------------------------------------------------
$raw = Get-Content -LiteralPath $manifestPath -Raw
$flows = $raw | ConvertFrom-Json

if ($flows -isnot [System.Collections.IEnumerable]) {
    $flows = @($flows)
}

$results = @()

# ---------------------------------------------------------------------------
# Run each enabled flow
# ---------------------------------------------------------------------------
foreach ($flow in $flows) {
    if (-not $flow.enabled) {
        continue
    }

    $id        = $flow.id
    $scriptRel = $flow.script
    $category  = $flow.category

    $scriptPath = Join-Path $repoRoot $scriptRel

    if (-not (Test-Path $scriptPath)) {
        Write-Host "[$id] MISSING script: $scriptPath" -ForegroundColor Red
        $results += [pscustomobject]@{
            id          = $id
            script      = $scriptRel
            category    = $category
            status      = "missing"
            duration_ms = 0
            error       = "Script not found"
        }
        continue
    }

    Write-Host "[$id] Running $scriptRel ..." -ForegroundColor Cyan

    $sw = [System.Diagnostics.Stopwatch]::StartNew()
    $status = "ok"
    $errorMsg = $null

    try {
        & $Python $scriptPath
        $exitCode = $LASTEXITCODE
        if ($exitCode -ne 0) {
            $status = "fail"
            $errorMsg = "Exit code $exitCode"
        }
    }
    catch {
        $status = "fail"
        $errorMsg = $_.Exception.Message
    }
    finally {
        $sw.Stop()
    }

    Write-Host "[$id] status=$status, duration=${($sw.ElapsedMilliseconds)}ms"

    $results += [pscustomobject]@{
        id          = $id
        script      = $scriptRel
        category    = $category
        status      = $status
        duration_ms = $sw.ElapsedMilliseconds
        error       = $errorMsg
    }
}

# ---------------------------------------------------------------------------
# Build summary JSON
# ---------------------------------------------------------------------------
$total = $results.Count
$ok    = ($results | Where-Object { $_.status -eq "ok" }).Count
$fail  = ($results | Where-Object { $_.status -eq "fail" }).Count
$missing = ($results | Where-Object { $_.status -eq "missing" }).Count

$summary = [pscustomobject]@{
    total_flows = $total
    successful  = $ok
    failed      = $fail
    missing     = $missing
    last_run    = (Get-Date).ToString("o")
    flows       = $results
}

$summaryJson = $summary | ConvertTo-Json -Depth 6
$summaryJson | Set-Content -LiteralPath $summaryPath -Encoding UTF8

Write-Host ""
Write-Host "Week-1 summary: total=$total, ok=$ok, failed=$fail, missing=$missing" -ForegroundColor Green
Write-Host "Summary written to $summaryPath"
