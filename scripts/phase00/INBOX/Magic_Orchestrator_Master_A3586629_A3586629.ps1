# =====================================================================
# MAGIC PROJECT – MASTER ORCHESTRATOR
# Runs ALL phases (00–17) in order and logs PASS/FAIL results
# =====================================================================

$rootPath = "scripts"
$logFile = "outputs\logs\Magic_Orchestrator_Master_Log.txt"
$csvFile = "outputs\logs\Magic_Orchestrator_Master_Results.csv"

"" | Out-File $logFile -Encoding UTF8
$results = @()

# Define ordered phases (00–17)
$phases = @(
    "phase0","phase1","phase2","phase3","phase4","phase5","phase6",
    "phase7","phase8","phase9","phase10","phase11","phase12",
    "phase13","phase14","phase15","phase16","phase17"
)

foreach ($phase in $phases) {
    Write-Host "🚀 Starting $phase"
    "`n=== PHASE: $phase ===" | Out-File -FilePath $logFile -Append -Encoding UTF8

    # Find all module folders inside this phase
    $modules = Get-ChildItem "$rootPath\$phase" -Directory -ErrorAction SilentlyContinue
    foreach ($module in $modules) {
        Write-Host "🔹 Running module: $($module.Name)"
        "`n--- MODULE: $($module.Name) ---" | Out-File -FilePath $logFile -Append -Encoding UTF8

        $scripts = Get-ChildItem -Path $module.FullName -Filter "*_READY.py" -File -ErrorAction SilentlyContinue | Sort-Object Name
        foreach ($script in $scripts) {
            Write-Host "▶ Executing: $($script.Name)"
            "`n>>> Running: $($script.Name) <<<" | Out-File -FilePath $logFile -Append -Encoding UTF8

            try {
                $output = & "$env:VIRTUAL_ENV\Scripts\python.exe" $script.FullName 2>&1
                if ($LASTEXITCODE -eq 0) {
                    $status = "PASS"
                    $msg = "Executed successfully"
                }
                else {
                    $status = "FAIL"
                    $msg = $output -join " "
                }
            }
            catch {
                $status = "FAIL"
                $msg = $_.Exception.Message
            }

            $results += [PSCustomObject]@{
                Phase      = $phase
                Module     = $module.Name
                ScriptName = $script.Name
                Status     = $status
                Message    = $msg
            }
        }
    }
}

$results | Export-Csv -Path $csvFile -NoTypeInformation -Encoding UTF8
Write-Host "✅ MASTER ORCHESTRATION COMPLETE. Results saved to $csvFile"
