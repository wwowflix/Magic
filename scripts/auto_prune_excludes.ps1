$inFile = ".\my_exclude_list.txt"
$outFile = ".\my_clean_exclude_list.txt"

if (Test-Path $inFile) {
    $lines = Get-Content $inFile
    $newLines = @()

    foreach ($line in $lines) {
        if ($line.Trim() -ne "") {
            $newLines += $line
        }
    }

    $newLines | Set-Content $outFile -Encoding UTF8
    Write-Host "Pruned exclude list. $($newLines.Count) items remain."
} else {
    Write-Host "Input file not found: $inFile"
}
