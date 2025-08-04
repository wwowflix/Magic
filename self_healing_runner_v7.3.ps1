# self_healing_runner_v7.3.ps1
param([string]$ManifestPath = ".\phase_manifest.json", [switch]$Force)

Write-Host "=== Starting Self-Healing Runner v7.3 ===`n"

$summary = @()
$manifest = Get-Content $ManifestPath | ConvertFrom-Json

foreach ($phase in $manifest.phases) {
    foreach ($module in $manifest.$phase.PSObject.Properties.Name) {
        $scripts = $manifest.$phase.$module
        foreach ($script in $scripts) {
            $scriptName = Split-Path $script -Leaf
            $logDir = "outputs/logs/$phase/$module"
            New-Item -ItemType Directory -Force -Path $logDir | Out-Null
            $logPath = "$logDir/$scriptName.log"

            Write-Host "▶ Running: $scriptName"
            try {
                $env:PYTHONIOENCODING="utf-8"
                python $script *> $logPath 2>&1
                if ($LASTEXITCODE -eq 0) {
                    Write-Host "✅ Success: $scriptName"
                    $summary += "✅ $scriptName"
                } else {
                    Write-Host "❌ Error: $scriptName (check log)"
                    $summary += "❌ $scriptName"
                }
            } catch {
                "Runner error: $($_.Exception.Message)" | Out-File -FilePath $logPath -Append
                $summary += "❌ $scriptName (Runner Error)"
            }
        }
    }
}

# Save summary
$summaryDir = "outputs/summaries"
New-Item -ItemType Directory -Force -Path $summaryDir | Out-Null
$summaryPath = "$summaryDir/runner_summary_$(Get-Date -Format 'yyyyMMdd_HHmmss').txt"
$summary | Out-File -FilePath $summaryPath -Encoding UTF8

Write-Host "`n=== ✅ Runner Complete ==="
Write-Host "📜 Summary saved to: $summaryPath"
