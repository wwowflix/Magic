# self_healing_runner_v7.1.ps1
param([string]$ManifestPath = ".\phase_manifest.json", [switch]$Force)

Write-Host "=== Starting Self-Healing Runner v7.1 ===`n"

$env:PYTHONIOENCODING = "utf-8"
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
                python -Xutf8 $script *> $logPath 2>&1
                if ($LASTEXITCODE -eq 0) {
                    Write-Host "✅ Success: $scriptName"
                } else {
                    Write-Host "❌ Error: $scriptName (check log)"
                }
            } catch {
                "Runner error: $($_.Exception.Message)" | Out-File -FilePath $logPath -Append
            }
        }
    }
}

Write-Host "`n=== Runner Complete ==="
