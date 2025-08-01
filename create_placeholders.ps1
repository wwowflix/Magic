# Load the cleaned CSV
$csvPath = "D:\MAGIC\Fulfinal_File_CLEANED.csv"
$data = Import-Csv -Path $csvPath

foreach ($row in $data) {
    $phase = $row.Phase
    $module = $row.Module
    $filename = $row.Filename

    if ([string]::IsNullOrWhiteSpace($phase) -or [string]::IsNullOrWhiteSpace($module) -or [string]::IsNullOrWhiteSpace($filename)) {
        Write-Host "Skipped row with missing data"
        continue
    }

    $targetFolder = "D:\MAGIC\scripts\phase$phase\module_$module"

    # Create the folder if it doesn't exist
    if (!(Test-Path -Path $targetFolder)) {
        New-Item -ItemType Directory -Path $targetFolder | Out-Null
    }

    $targetFile = Join-Path -Path $targetFolder -ChildPath $filename

    # Only create the file if it doesn't already exist
    if (!(Test-Path -Path $targetFile)) {
        New-Item -ItemType File -Path $targetFile | Out-Null
        Write-Host "Created blank file: $targetFile"
    } else {
        Write-Host "Already exists: $targetFile"
    }
}
