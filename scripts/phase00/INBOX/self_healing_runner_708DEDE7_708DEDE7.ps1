# ===========================
# Self-Healing Runner - Week 2
# Production-Readiness: Logging, Summaries & Retry
# ===========================
# Reads phase_manifest.json, runs scripts, logs results,
# retries failures, and produces summary reports.

$manifestPath = "D:\MAGIC\phase_manifest.json"
$logRoot = "D:\MAGIC\outputs\logs"
$summaryRoot = "D:\MAGIC\outputs\summaries"

# Ensure directories exist
if (!(Test-Path $logRoot)) { New-Item -ItemType Directory -Path $logRoot | Out-Null }
if (!(Test-Path $summaryRoot)) { New-Item -ItemType Directory -Path $summaryRoot | Out-Null }

# Load manifest
if (!(Test-Path $manifestPath)) {
    Write-Host "❌ Manifest file not found at $manifestPath"
    exit 1
}

$jsonRaw = Get-Content $manifestPath -Raw
if ([string]::IsNullOrWhiteSpace($jsonRaw)) {
    Write-Host "❌ Manifest file is empty."
    exit 1
}

try {
    $manifestContent = $jsonRaw | ConvertFrom-Json
}
catch {
    Write-Host "❌ Failed to parse JSON: $($_.Exception.Message)"
    exit 1
}

# Track results for master summary
$results = @()

foreach ($entry in $manifestContent) {
    $phase = $entry.Phase
    $module = $entry.Module
    $script = $entry.Script
    $scriptPath = Join-Path "D:\MAGIC" $entry.Path

    $logDir = Join-Path $logRoot "phase${phase}_module_${module}"
    if (!(Test-Path $logDir)) { New-Item -ItemType Directory -Path $logDir | Out-Null }

    $logFile = Join-Path $logDir "$script.log"

    Write-Host "`n=== Phase $phase - Module $module ==="
    Write-Host "▶ Running: $script"

    $status = "ERROR"
    $attempt = 0
    $maxRetries = 2

    while ($attempt -le $maxRetries) {
        $attempt++
        try {
            if (!(Test-Path $scriptPath)) {
                Write-Host "[WARNING] Script not found: $scriptPath"
                "NOT_FOUND" | Out-File $logFile
                break
            }

            & python $scriptPath 1>> $logFile 2>&1
            $exitCode = $LASTEXITCODE

            if ($exitCode -eq 0) {
                Write-Host "✅ Success on attempt $attempt"
                $status = "OK"
                break
            } else {
                Write-Host "❌ Failed (exit code $exitCode) on attempt $attempt"
            }
        }
        catch {
            Write-Host ("[WARNING] Exception on attempt {0}: {1}" -f $attempt, $_.Exception.Message)
            "EXCEPTION: $($_.Exception.Message)" | Out-File -Append $logFile
        }
    }

    # Append result
    $results += [PSCustomObject]@{
        Phase  = $phase
        Module = $module
        Script = $script
        Status = $status
    }

    # Per-module summary
    $summaryFile = Join-Path $summaryRoot "summary_phase${phase}_module_${module}.tsv"
    "$phase`t$module`t$script`t$status" | Out-File -Append $summaryFile
}

# Write master summary
$masterSummary = Join-Path $summaryRoot "phase_master_summary.tsv"
"Phase`tModule`tScript`tStatus" | Out-File $masterSummary
$results | ForEach-Object {
    "$($_.Phase)`t$($_.Module)`t$($_.Script)`t$($_.Status)"
} | Out-File -Append $masterSummary

Write-Host "`n✅ Runner execution complete. Logs in outputs/logs/, summaries in outputs/summaries/"
