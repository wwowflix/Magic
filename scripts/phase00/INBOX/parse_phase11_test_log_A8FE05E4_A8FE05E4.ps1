$logFile = "outputs\logs\phase11_autoheal_test_log.txt"
$outputCsv = "outputs\logs\phase11_test_summary.csv"

if (!(Test-Path $logFile)) {
    Write-Host "❌ Log file not found: $logFile"
    exit
}

$results = @()
$currentScript = ""

Get-Content $logFile | ForEach-Object {
    if ($_ -match '^=== Testing: (.+) ===$') {
        $currentScript = $matches[1]
    }
    elseif ($_ -match '^EXCEPTION: (.+)$') {
        $results += [PSCustomObject]@{
            ScriptName = $matches[1]
            Status     = "FAIL"
            Message    = "Exception occurred"
        }
    }
    elseif ($_ -match '^Already valid: (.+)$') {
        $results += [PSCustomObject]@{
            ScriptName = $matches[1]
            Status     = "PASS"
            Message    = "Placeholder already valid"
        }
    }
    elseif ($_ -match '^Testing all Phase 11 scripts') {
        # Skip
    }
}

if ($results.Count -eq 0) {
    Write-Host "⚠️ No results found in log file." -ForegroundColor Yellow
} else {
    $results | Export-Csv -Path $outputCsv -NoTypeInformation -Encoding UTF8
    Write-Host "✅ Summary generated: $outputCsv"
}
