# ============================
# MAGIC MASTER ORCHESTRATOR v2
# ============================
# Purpose:
# - Runs all _READY.py scripts in Phase 11
# - Captures PASS / FAIL for each script
# - Saves results to summary log
# - Easy-to-read output in PowerShell

$phasePath = "D:\MAGIC\scripts\phase11"
$logFile   = "D:\MAGIC\outputs\logs\master_orchestrator_log.txt"
$summary   = "D:\MAGIC\outputs\logs\master_orchestrator_summary.txt"

# Clear previous logs
"" | Out-File $logFile -Encoding UTF8
"" | Out-File $summary -Encoding UTF8

Write-Host "🚀 Starting MAGIC Phase 11 Orchestration..." -ForegroundColor Cyan

# Collect results
$results = @()

# Loop through scripts
Get-ChildItem -Path $phasePath -Recurse -Filter "*_READY.py" | Sort-Object Name | ForEach-Object {
    $scriptPath = $_.FullName
    $scriptName = $_.Name

    # Log start
    "`n>>> Running: $scriptName <<<" | Tee-Object -FilePath $logFile -Append

    try {
        # Run script and capture result
        $output = & python "$scriptPath" 2>&1

        if ($LASTEXITCODE -eq 0 -and $output -match "PASS") {
            $status = "✅ PASS"
        }
        elseif ($LASTEXITCODE -eq 0 -and $output -match "FAIL") {
            $status = "❌ FAIL"
        }
        else {
            $status = "⚠️ UNKNOWN"
        }

        # Append to log
        $output | Out-File -FilePath $logFile -Append -Encoding UTF8
        $results += [PSCustomObject]@{
            Script = $scriptName
            Status = $status
        }
    }
    catch {
        $results += [PSCustomObject]@{
            Script = $scriptName
            Status = "❌ ERROR"
        }
    }
}

# Save summary table
"====================" | Out-File $summary -Append
" PHASE 11 - TEST SUMMARY" | Out-File $summary -Append
"====================" | Out-File $summary -Append
$results | Format-Table | Out-String | Out-File $summary -Append -Encoding UTF8

Write-Host "`n✅ MASTER ORCHESTRATION COMPLETE."
Write-Host "Summary saved to $summary" -ForegroundColor Green
