# Cleanup Agent for MAGIC Project
# Archives old logs, compresses big logs, and deletes test scripts from Phase99.

Write-Host "🔄 Starting cleanup process..."

$logPath = "D:\MAGIC\outputs\logs"
$summaryPath = "D:\MAGIC\outputs\summaries"
$testPath = "D:\MAGIC\scripts\phase99\module_ZZ"
$archivePath = "D:\MAGIC\logs\archive"

# 1️⃣ Ensure archive folder exists
if (!(Test-Path $archivePath)) {
    New-Item -ItemType Directory -Path $archivePath | Out-Null
}

# 2️⃣ Archive old logs (older than 7 days)
$oldLogs = Get-ChildItem -Path $logPath -Recurse -Include *.log | Where-Object { $_.LastWriteTime -lt (Get-Date).AddDays(-7) }
foreach ($log in $oldLogs) {
    Move-Item $log.FullName -Destination $archivePath -Force
    Write-Host "🗄 Archived log: $($log.Name)"
}

# 3️⃣ Compress logs larger than 5MB
$largeLogs = Get-ChildItem -Path $logPath -Recurse -Include *.log | Where-Object { $_.Length -gt 5MB }
foreach ($bigLog in $largeLogs) {
    Compress-Archive -Path $bigLog.FullName -DestinationPath "$($bigLog.FullName).zip" -Force
    Remove-Item $bigLog.FullName -Force
    Write-Host "📦 Compressed large log: $($bigLog.Name)"
}

# 4️⃣ Delete test scripts from Phase99
if (Test-Path $testPath) {
    $testFiles = Get-ChildItem -Path $testPath -Filter "*test_error*.py"
    foreach ($file in $testFiles) {
        Remove-Item $file.FullName -Force
        Write-Host "🗑 Deleted test script: $($file.Name)"
    }
}

Write-Host "✅ Cleanup complete."
