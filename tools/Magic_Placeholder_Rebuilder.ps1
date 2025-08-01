param(
    [string]$csvPath = "D:\Final_File_FOR_Automate.csv",
    [string]$rootPath = "D:\MAGIC\scripts"
)

Write-Host "Starting Placeholder Rebuilder..."

# 1️⃣ Delete old placeholder files (_READY.py only)
Write-Host "Cleaning old placeholders..."
Get-ChildItem -Path $rootPath -Recurse -Filter "*_READY.py" -File |
    Remove-Item -Force

# 2️⃣ Read CSV and loop through entries
$csv = Import-Csv $csvPath
$report = @()

foreach ($row in $csv) {
    $phase = $row.PhaseNumber
    $module = "module_" + $row.Module
    $filename = $row.FinalFilename

    $phaseFolder = Join-Path $rootPath ("phase" + $phase)
    $moduleFolder = Join-Path $phaseFolder $module

    # Ensure folder exists
    if (!(Test-Path $moduleFolder)) {
        New-Item -ItemType Directory -Path $moduleFolder -Force | Out-Null
    }

    # Placeholder path
    $filePath = Join-Path $moduleFolder $filename

    if (!(Test-Path $filePath)) {
        New-Item -ItemType File -Path $filePath -Force | Out-Null
        Add-Content -Path $filePath -Value "# Placeholder for $filename"
        $report += "ADDED: $phase/$module/$filename"
    }
    else {
        $report += "EXISTS: $phase/$module/$filename"
    }
}

# 3️⃣ Write final report
$reportFile = "D:\MAGIC\outputs\placeholder_rebuild_report.txt"
$report | Out-File -FilePath $reportFile -Encoding UTF8

Write-Host "Placeholder rebuild complete! Report saved to $reportFile"
