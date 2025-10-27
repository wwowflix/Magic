# ===============================================================
# PHASE 11 ORCHESTRATOR
# Runs all Phase 11 scripts module by module in order (A → Z → AA → AB)
# Logs execution results to a CSV file
# ===============================================================

$phase11Path = "scripts\phase11"
$logFile = "outputs\logs\phase11_orchestrator_log.txt"
$csvFile = "outputs\logs\phase11_orchestrator_results.csv"

"" | Out-File $logFile -Encoding UTF8
$results = @()

# Define execution order manually (to enforce module order)
$moduleOrder = @(
    "module_A","module_B","module_C","module_D","module_E","module_F","module_G",
    "module_H","module_I","module_J","module_K","module_L","module_M","module_N",
    "module_O","module_P","module_Q","module_R","module_S","module_T","module_U",
    "module_V","module_W","module_X","module_Y","module_Z","module_AA","module_AB"
)

foreach ($module in $moduleOrder) {
    Write-Host "🚀 Running module: $module"
    "`n=== Module: $module ===" | Out-File -FilePath $logFile -Append -Encoding UTF8

    $scripts = Get-ChildItem -Path "$phase11Path\$module" -Filter "*_READY.py" -File | Sort-Object Name
    foreach ($script in $scripts) {
        Write-Host "▶ Executing: $($script.Name)"
        "`n--- Running: $($script.Name) ---" | Out-File -FilePath $logFile -Append -Encoding UTF8

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
            Module     = $module
            ScriptName = $script.Name
            Status     = $status
            Message    = $msg
        }
    }
}

$results | Export-Csv -Path $csvFile -NoTypeInformation -Encoding UTF8
Write-Host "✅ Orchestration complete. Results saved to $csvFile"
