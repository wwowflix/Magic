param(
  [string]$Root = "D:\MAGIC",
  [int]$LogDays = 7,
  [int]$LargeMB = 50
)

$ErrorActionPreference = 'Stop'
Set-Location $Root

$reportDir = Join-Path $Root "outputs\reports"
New-Item -ItemType Directory -Force -Path $reportDir | Out-Null
$tsv = Join-Path $reportDir "cleanup_plan.tsv"
$md  = Join-Path $reportDir "cleanup_plan.md"

function Row($Type,$Path,$Reason,$SizeBytes,$AgeDays){
  [PSCustomObject]@{
    Type=$Type; Path=$Path; Reason=$Reason
    SizeMB = if($SizeBytes){ [math]::Round($SizeBytes/1MB,2) } else { "" }
    AgeDays = $AgeDays
  }
}

$rows = New-Object System.Collections.Generic.List[object]

# 1) Editor/system junk
$patterns = @('Thumbs.db','.DS_Store','desktop.ini')
Get-ChildItem -Recurse -File -ErrorAction SilentlyContinue |
  Where-Object { $patterns -contains $_.Name } |
  ForEach-Object { $rows.Add((Row "junk" $_.FullName "editor/system junk" $_.Length $null)) }

# 2) __pycache__ / pyc
Get-ChildItem -Recurse -Directory -Filter "__pycache__" -ErrorAction SilentlyContinue |
  ForEach-Object { $rows.Add((Row "cache-dir" $_.FullName "Python bytecode cache dir" $null $null)) }
Get-ChildItem -Recurse -File -Include *.pyc,*.pyo -ErrorAction SilentlyContinue |
  ForEach-Object { $rows.Add((Row "bytecode" $_.FullName "Compiled Python bytecode" $_.Length $null)) }

# 3) Temp/duplicates
$dupRegex = '(?i)(^|[ _.-])(copy|tmp|temp|backup|bak|~\$)|\(\d+\)'
Get-ChildItem -Recurse -File -ErrorAction SilentlyContinue |
  Where-Object { $_.Name -match $dupRegex } |
  ForEach-Object { $rows.Add((Row "dup-temp" $_.FullName "looks like duplicate/temp" $_.Length $null)) }

# 4) Garbled filenames
$garble = '├|â|┬|ô|Γ|Ç|â€“|Ã'
Get-ChildItem -Recurse -File -ErrorAction SilentlyContinue |
  Where-Object { $_.Name -match $garble } |
  ForEach-Object { $rows.Add((Row "garbled" $_.FullName "suspect encoding in filename" $_.Length $null)) }

# 5) Old logs
$logRoot = Join-Path $Root "outputs\logs"
if (Test-Path $logRoot) {
  Get-ChildItem $logRoot -Recurse -File -ErrorAction SilentlyContinue |
    Where-Object { $_.LastWriteTime -lt (Get-Date).AddDays(-$LogDays) } |
    ForEach-Object {
      $age = [int]((Get-Date) - $_.LastWriteTime).TotalDays
      $rows.Add((Row "old-log" $_.FullName "older than $LogDays days" $_.Length $age))
    }
}

# 6) Backups: keep newest per folder
$backupRoot = Join-Path $Root "backups"
if (Test-Path $backupRoot) {
  Get-ChildItem $backupRoot -Recurse -File -ErrorAction SilentlyContinue |
    Group-Object { $_.DirectoryName } | ForEach-Object {
      $sorted = $_.Group | Sort-Object LastWriteTime -Descending
      $keep = $sorted | Select-Object -First 1
      $sorted | Select-Object -Skip 1 | ForEach-Object {
        $age = [int]((Get-Date) - $_.LastWriteTime).TotalDays
        $rows.Add((Row "old-backup" $_.FullName "older than newest in folder; keep: $($keep.Name)" $_.Length $age))
      }
    }
}

# 7) Large output files
$outRoot = Join-Path $Root "outputs"
if (Test-Path $outRoot) {
  Get-ChildItem $outRoot -Recurse -File -ErrorAction SilentlyContinue |
    Where-Object { $_.Length -gt ($LargeMB * 1MB) } |
    ForEach-Object {
      $rows.Add((Row "large-output" $_.FullName "larger than ${LargeMB}MB" $_.Length $null))
    }
}

# 8) Zero-byte files
Get-ChildItem -Recurse -File -ErrorAction SilentlyContinue |
  Where-Object { $_.Length -eq 0 } |
  ForEach-Object { $rows.Add((Row "zero-byte" $_.FullName "empty file" 0 $null)) }

# 9) Stray reports
Get-ChildItem -Recurse -File -Include *.tsv,*.md,*.json -ErrorAction SilentlyContinue |
  Where-Object { $_.FullName -notlike (Join-Path $reportDir "*") } |
  ForEach-Object { $rows.Add((Row "stray-report" $_.FullName "report-like file outside outputs/reports" $_.Length $null)) }

# Save TSV
$rows | Sort-Object Type, Path |
  Export-Csv -Path $tsv -Delimiter "`t" -NoTypeInformation -Encoding UTF8

# Save Markdown summary
$counts = $rows | Group-Object Type | ForEach-Object { "| {0} | {1} |" -f $_.Name, $_.Count }
@(
  "# MAGIC – Cleanup Plan (dry-run)"
  ""
  "**Root:** $Root"
  ""
  "| Type | Count |"
  "|------|------:|"
  $counts
  ""
  "Full list: ``outputs/reports/cleanup_plan.tsv``"
) -join "`r`n" | Out-File -FilePath $md -Encoding UTF8

Write-Host "`nPlanned cleanup (dry-run) written to:" -ForegroundColor Cyan
Write-Host " - $tsv"
Write-Host " - $md"
$rows | Group-Object Type | Sort-Object Name | ForEach-Object { "{0,12} : {1,5}" -f $_.Name, $_.Count } | Write-Host
