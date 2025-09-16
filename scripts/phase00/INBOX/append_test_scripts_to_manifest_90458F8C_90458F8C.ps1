$manifestPath = "D:\MAGIC\phase_manifest.json"

# Load existing manifest JSON
if (-Not (Test-Path $manifestPath)) {
    Write-Error "Manifest file not found at $manifestPath"
    exit 1
}

$jsonRaw = Get-Content $manifestPath -Raw
try {
    $manifest = $jsonRaw | ConvertFrom-Json
} catch {
    Write-Error "Failed to parse manifest JSON: $_"
    exit 1
}

# Define new test script entries to add
$testScripts = @(
    [PSCustomObject]@{
        PhaseNumber = 99
        Module = "ZZ"
        FinalFilename = "D:\\MAGIC\\scripts\\phase99\\module_ZZ\\file_not_found_test.py"
    },
    [PSCustomObject]@{
        PhaseNumber = 99
        Module = "ZZ"
        FinalFilename = "D:\\MAGIC\\scripts\\phase99\\module_ZZ\\unicode_error_test.py"
    },
    [PSCustomObject]@{
        PhaseNumber = 99
        Module = "ZZ"
        FinalFilename = "D:\\MAGIC\\scripts\\phase99\\module_ZZ\\import_error_test.py"
    }
)

# Append test entries to manifest array
$updatedManifest = $manifest + $testScripts

# Convert back to JSON with indentation
$jsonOut = $updatedManifest | ConvertTo-Json -Depth 10 -Compress:$false

# Save updated manifest
Set-Content -Path $manifestPath -Value $jsonOut -Encoding UTF8

Write-Host "Test scripts appended successfully to $manifestPath"
