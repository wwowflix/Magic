param(
    [string]$ManifestPath = "phase_manifest.json"
)

Write-Host "=== Starting Self-Healing Runner v6.7 ==="

if (-Not (Test-Path $ManifestPath)) {
    Write-Error "Manifest file not found: $ManifestPath"
    exit 1
}

try {
    $manifest = Get-Content $ManifestPath -Raw | ConvertFrom-Json
} catch {
    Write-Error "❌ Failed to read or parse manifest file: $_"
    exit 1
}

foreach ($entry in $manifest) {
    $scriptPath = $entry.path
    $scriptName = $entry.FinalFilename

    if (Test-Path $scriptPath) {
        Write-Host "▶ Running: $scriptName"
        try {
            python $scriptPath | Tee-Object -FilePath "outputs/logs/$scriptName.log"
            Write-Host "✅ Success: $scriptName"
        } catch {
            Write-Warning "⚠️ Error running script: $scriptName"
        }
    } else {
        Write-Warning "⚠️ Script not found: $scriptName"
    }
}

Write-Host "=== Runner Complete ==="
