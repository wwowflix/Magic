# Load the cleaned CSV
$data = Import-Csv -Path "D:\MAGIC\Fullfinal_File_CLEANED.csv"

foreach ($row in $data) {
    $phase = $row.Phase.Trim()
    $module = $row.Module.Trim()
    $sourceFile = $row.'Original Path'.Trim()
    $filename = $row.Filename.Trim()
    $targetFolder = "D:\MAGIC\scripts\phase$phase\module_$module"
    $destFile = Join-Path $targetFolder $filename

    if (!(Test-Path -Path $targetFolder)) {
        New-Item -ItemType Directory -Path $targetFolder -Force | Out-Null
    }

    # If placeholder exists, back it up before replacing
    if (Test-Path $destFile) {
        $backupFolder = "D:\MAGIC\backups\phase$phase\module_$module"
        if (!(Test-Path -Path $backupFolder)) {
            New-Item -ItemType Directory -Path $backupFolder -Force | Out-Null
        }
        Copy-Item -Path $destFile -Destination $backupFolder -Force
        Write-Host "🛡️ Placeholder backed up: $filename"
    }

    # Move actual file from inbox/approved
    Move-Item -Path $sourceFile -Destination $destFile -Force
    Write-Host "✅ Moved: $filename → $targetFolder"
}
