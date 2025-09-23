param(
    [string]$Manifest = "phase_manifest.json",
    [switch]$CleanLogs
)

if ($CleanLogs) {
    Write-Host "Cleaning outputs/logs/..."
    Remove-Item -Recurse -Force .\outputs\logs -ErrorAction SilentlyContinue
}

Write-Host "Generating phase_manifest.json..."
python .\generate_manifest.py

Write-Host "Running self_healing_runner.py..."
python .\self_healing_runner.py --manifest $Manifest

Write-Host ""
Write-Host "All done!"
