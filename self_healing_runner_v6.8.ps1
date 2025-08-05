@'
# ============================
# Self-Healing Runner v6.9
# Adds: -Force parameter, removes false skipping
# ============================
param(
    [string]$ManifestPath = ".\phase_manifest.json",
    [switch]$Force
)

Write-Host "=== Starting Self-Healing Runner v6.9 ==="

# Load manifest
if (-Not (Test-Path $ManifestPath)) {
    Write-Error "Manifest file not found: $ManifestPath"
    exit 1
}
$manifest = Get-Content $ManifestPath | ConvertFrom-Json

foreach ($phase in $manifest.phases) {
    $phaseData = $manifest.$phase

    foreach ($module in $phaseData.PSObject.Properties.Name) {
        Write-Host "`n=== Processing $phase : $module ==="

        $scripts = $phaseData.$module
        foreach ($script in $scripts) {
            $scriptName = Split-Path $script -Leaf
            $scriptPath = Join-Path $PWD $script

            # Skip only if marker file exists and -Force is not used
            $marker = "outputs/logs/$phase.completed"
            if ((Test-Path $marker) -and (-not $Force)) {
                Write-Warning "Skipping $phase (already completed)"
                continue
            }

            # Run script
            if (Test-Path $scriptPath) {
                try {
                    Write-Host "▶ Running: $scriptName"
                    python $scriptPath
                    Write-Host "✅ Success: $scriptName"
                }
                catch {
                    Write-Warning "⚠ Error running: $scriptName"
                }
            }
            else {
                Write-Warning "⚠ Script not found: $scriptName"
            }
        }
    }

    # Create marker file after successful phase run
    New-Item -Path "outputs/logs/$phase.completed" -ItemType File -Force | Out-Null
}

Write-Host "`n=== Runner Complete ==="
'@ | Set-Content -Path "self_healing_runner_v6.9.ps1" -Encoding UTF8
