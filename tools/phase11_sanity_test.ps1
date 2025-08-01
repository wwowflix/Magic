$logFile = "outputs/logs/phase11_sanity_test.txt"
"" | Out-File $logFile -Encoding utf8

Get-ChildItem -Path "scripts\phase11" -Recurse -Filter "*_READY.py" |
Sort-Object Name |
ForEach-Object {
    $file = $_.FullName
    $name = $_.Name

    "=== Testing: $name ===" | Tee-Object -FilePath $logFile -Append

    try {
        & "$env:VIRTUAL_ENV\Scripts\python.exe" "$file" 2>&1 | Tee-Object -FilePath $logFile -Append
        if ($LASTEXITCODE -eq 0) {
            "PASS: $name" | Tee-Object -FilePath $logFile -Append
        } else {
            "FAIL (exit code $LASTEXITCODE): $name" | Tee-Object -FilePath $logFile -Append
        }
    } catch {
        "EXCEPTION: $name" | Tee-Object -FilePath $logFile -Append
    }

    "------------------------" | Tee-Object -FilePath $logFile -Append
}

Write-Host "Test report saved to $logFile"
