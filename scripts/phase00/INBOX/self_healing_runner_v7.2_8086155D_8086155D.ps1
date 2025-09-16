# self_healing_runner_v7.2.ps1
param([string]$ManifestPath = ".\phase_manifest.json", [switch]$Force)

Write-Host "=== 🚀 Starting Self-Healing Runner v7.2 ===`n" -ForegroundColor Cyan

# Load manifest
$manifest = Get-Content $ManifestPath | ConvertFrom-Json

# Clean up old logs and summaries for selected phases
foreach ($phase in $manifest.phases) {
    $logDir = "outputs/logs/$phase"
    $sumDir = "outputs/summaries/$phase"
    if (Test-Path $logDir) { Remove-Item $logDir -Recurse -Force -ErrorAction SilentlyContinue }
    if (Test-Path $sumDir) { Remove-Item $sumDir -Recurse -Force -ErrorAction SilentlyContinue }
}

# Run scripts
foreach ($phase in $manifest.phases) {
    foreach ($module in $manifest.$phase.PSObject.Properties.Name) {
        $scripts = $manifest.$phase.$module
        foreach ($script in $scripts) {
            $scriptName = Split-Path $script -Leaf
            $logDir = "outputs/logs/$phase/$module"
            New-Item -ItemType Directory -Force -Path $logDir | Out-Null
            $logPath = "$logDir/$scriptName.log"

            Write-Host "▶ Running: $scriptName" -ForegroundColor Yellow
            try {
                $env:PYTHONIOENCODING = "utf-8"
                python $script *> $logPath 2>&1
                if ($LASTEXITCODE -eq 0) {
                    Write-Host "✅ Success: $scriptName" -ForegroundColor Green
                } else {
                    Write-Host "❌ Error: $scriptName (check log)" -ForegroundColor Red
                }
            } catch {
                "Runner error: $($_.Exception.Message)" | Out-File -FilePath $logPath -Append
            }
        }
    }

    # Mark phase completed
    "Phase $phase completed at $(Get-Date)" | Out-File "outputs/logs/$phase.completed"
}

Write-Host "`n=== ✅ Runner Complete ===" -ForegroundColor Cyan
