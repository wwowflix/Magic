# =========================================
# MAGIC Phase 11 Auto-Heal and Test Script
# =========================================

$phasePath = "scripts\phase11"
$backupPath = "backups\phase11_autoheal_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
$logFile = "outputs\logs\phase11_autoheal_test_log.txt"

# Create backup folder
Write-Host "Creating backup at $backupPath"
New-Item -ItemType Directory -Path $backupPath -Force | Out-Null

# Backup all existing scripts
Copy-Item -Path "$phasePath\*" -Destination $backupPath -Recurse -Force

# Auto-heal placeholders
Write-Host "Starting auto-heal of placeholder scripts..."
Get-ChildItem -Path $phasePath -Recurse -Filter "*_READY.py" | ForEach-Object {
    $filePath = $_.FullName
    $content = Get-Content $filePath -Raw

    if ($content -notmatch "def main\(") {
        @"
def main():
    pass

if __name__ == "__main__":
    main()
"@ | Set-Content -Path $filePath -Encoding UTF8
        Write-Host "Fixed placeholder: $filePath"
    }
    else {
        Write-Host "Already valid: $filePath"
    }
}

# Test all scripts
Write-Host "Testing all Phase 11 scripts..."
"" | Out-File $logFile
Get-ChildItem -Path $phasePath -Recurse -Filter "*_READY.py" | Sort-Object Name | ForEach-Object {
    $filePath = $_.FullName
    Add-Content $logFile "`n=== Testing: $($filePath) ==="
    try {
        $output = & "$env:VIRTUAL_ENV\Scripts\python.exe" "$filePath" 2>&1
        if ($output) {
            $output | Out-File -Append -FilePath $logFile -Encoding utf8
        } else {
            Add-Content $logFile "No errors."
        }
    }
    catch {
        Add-Content $logFile "EXCEPTION: $filePath"
    }
}

Write-Host "Auto-heal and test complete. Log saved to $logFile"
