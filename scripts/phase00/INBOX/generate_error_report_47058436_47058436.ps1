$logFolder = ".\outputs\logs"
$outputCsv = ".\outputs\error_report.csv"

# Keywords to search for in logs
$errorKeywords = @("error", "exception", "traceback")

# Find all .log files recursively
$logFiles = Get-ChildItem -Path $logFolder -Recurse -Filter *.log

# Initialize an array for storing error entries
$errorEntries = @()

foreach ($logFile in $logFiles) {
    foreach ($keyword in $errorKeywords) {
        $matches = Select-String -Path $logFile.FullName -Pattern $keyword -CaseSensitive:$false
        foreach ($match in $matches) {
            $errorEntries += [PSCustomObject]@{
                LogFile     = $logFile.FullName
                LineNumber  = $match.LineNumber
                Keyword     = $keyword
                LineText    = $match.Line.Trim()
            }
        }
    }
}

if ($errorEntries.Count -gt 0) {
    $errorEntries | Sort-Object LogFile, LineNumber | Export-Csv -Path $outputCsv -NoTypeInformation -Encoding UTF8
    Write-Host "✅ Error report generated at $outputCsv with $($errorEntries.Count) entries."
} else {
    Write-Host "✅ No errors found in logs."
}
