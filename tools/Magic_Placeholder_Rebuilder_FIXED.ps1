param (
    [string]$csvPath = "D:\Final_File_FOR_Automate.csv",
    [string]$scriptsRoot = "D:\MAGIC\scripts",
    [string]$reportPath = "D:\MAGIC\outputs\placeholder_rebuild_report.txt"
)

Write-Host "`n🧹 Deleting old _READY.py placeholders from phase11..."
Get-ChildItem "$scriptsRoot\phase11" -Recurse -Filter "*_READY.py" -File | Remove-Item -Force

Write-Host "📄 Reading CSV: $csvPath"
$csv = Import-Csv $csvPath
$log = @()

foreach ($row in $csv) {
    if ($row.PhaseNumber -eq "11" -and $row.FinalFilename) {
        $modLetter = $row.Module.Trim()
        $moduleName = "module_" + $modLetter
        $targetFolder = Join-Path "$scriptsRoot\phase11" $moduleName
        $targetFile = Join-Path $targetFolder $row.FinalFilename

        if (!(Test-Path $targetFolder)) {
            New-Item -ItemType Directory -Path $targetFolder -Force | Out-Null
        }

        if (!(Test-Path $targetFile)) {
            New-Item -ItemType File -Path $targetFile -Force | Out-Null
            Add-Content -Path $targetFile -Value "# Placeholder for $($row.FinalFilename)"
            $log += "✅ ADDED: $moduleName\$($row.FinalFilename)"
        }
        else {
            $log += "✔️ EXISTS: $moduleName\$($row.FinalFilename)"
        }
    }
}

$log | Out-File -FilePath $reportPath -Encoding UTF8
Write-Host "`n🎉 Done! Report saved to:`n$reportPath"
