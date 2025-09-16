param (
    [string]$ProjectRoot = "D:\MAGIC",
    [string]$ManifestPath = "D:\MAGIC\phase_manifest.json"
)

Write-Host "Scanning project folders..." -ForegroundColor Cyan

$manifest = @()

# Loop through all *_READY.py scripts
Get-ChildItem -Path "$ProjectRoot\scripts" -Recurse -Filter "*_READY.py" | ForEach-Object {
    $relativePath = $_.FullName.Replace("$ProjectRoot\", "")
    $phase = ($relativePath -split '\\')[1]
    $module = ($relativePath -split '\\')[2]
    $script = $_.Name

    $manifest += [PSCustomObject]@{
        Phase   = $phase
        Module  = $module
        Script  = $script
        Path    = $relativePath
    }
}

# Save manifest as JSON
$manifest | ConvertTo-Json -Depth 5 | Out-File $ManifestPath -Encoding utf8

Write-Host "Manifest saved to $ManifestPath" -ForegroundColor Green

# Create placeholder files for missing scripts (phase 0–18, modules A–Z)
$allPhases = 0..18
$allModules = @()
65..90 | ForEach-Object { $allModules += [char]$_ }

foreach ($p in $allPhases) {
    foreach ($m in $allModules) {
        $moduleFolder = "$ProjectRoot\scripts\phase$p\module_$m"
        if (-not (Test-Path $moduleFolder)) {
            New-Item -ItemType Directory -Path $moduleFolder -Force | Out-Null
        }

        # Define placeholder filename
        $placeholderFile = "$moduleFolder\$($p)$($m)_placeholder_READY.py"
        if (-not (Test-Path $placeholderFile)) {
            Set-Content -Path $placeholderFile -Value "# Placeholder script for Phase $p Module $m`nprint('Phase $p Module $m placeholder executed')" -Encoding utf8
        }
    }
}

Write-Host "Placeholders created where needed." -ForegroundColor Green
