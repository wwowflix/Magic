$summaryPath = "outputs\summaries\phase_master_summary.tsv"
$backupRoot = "backups"

# Read the summary file, skipping the header
$lines = Get-Content $summaryPath | Select-Object -Skip 1

foreach ($line in $lines) {
    $cols = $line -split "`t"
    $phase = $cols[0]
    $module = $cols[1]
    $script = $cols[2]
    $status = $cols[3]

    if ($status -eq "FAIL") {
        $scriptPath = "scripts\phase$phase\module_$module\$script"
        if (Test-Path $scriptPath) {
            $backupDir = Join-Path $backupRoot "phase$phase\module_$module"
            New-Item -ItemType Directory -Force -Path $backupDir | Out-Null
            Copy-Item $scriptPath -Destination $backupDir -Force
            Write-Host "📦 Backed up $script to $backupDir"
        } else {
            Write-Host "❌ Script not found: $scriptPath"
        }
    }
}
