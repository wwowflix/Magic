$phase11Path = "scripts\phase11"
$logFile = "outputs\logs\phase11_master_test_log.txt"
$csvFile = "outputs\logs\phase11_master_test_results.csv"

"" | Out-File $logFile -Encoding UTF8
$results = @()

Get-ChildItem -Path $phase11Path -Recurse -Filter "*_READY.py" | Sort-Object Name | ForEach-Object {
    $scriptName = $_.Name
    Write-Host "▶ Testing: $scriptName"
    "`n=== Testing: $scriptName ===" | Out-File -FilePath $logFile -Append -Encoding UTF8

    try {
        $output = & "$env:VIRTUAL_ENV\Scripts\python.exe" $_.FullName 2>&1
        if ($LASTEXITCODE -eq 0) {
            $status = "PASS"
            $msg = "Executed successfully"
        }
        else {
            $status = "FAIL"
            $msg = $output -join " "
        }
    }
    catch {
        $status = "FAIL"
        $msg = $_.Exception.Message
    }

    $results += [PSCustomObject]@{
        ScriptName = $scriptName
        Status     = $status
        Message    = $msg
    }
}

$results | Export-Csv -Path $csvFile -NoTypeInformation -Encoding UTF8
Write-Host "✅ Test run complete. Results saved to $csvFile"
