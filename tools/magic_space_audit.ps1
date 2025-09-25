<#
.SYNOPSIS
  SPACE AUDIT for MAGIC — categories + totals (repeatable, safe).

.USAGE
  powershell -NoProfile -ExecutionPolicy Bypass `
    -File .\tools\magic_space_audit.ps1 -Root "D:\MAGIC" -TopN 20
#>

param(
  [string]$Root = (Get-Location).Path,
  [int]$TopN = 20
)

# Helpers
function Ensure-Dir([string]$p) { if (-not (Test-Path $p)) { New-Item -ItemType Directory -Force -Path $p | Out-Null } }
function Get-FolderMB([string]$p) {
  if (-not (Test-Path $p)) { return 0.0 }
  try {
    $sum = (Get-ChildItem -LiteralPath $p -Recurse -File -ErrorAction SilentlyContinue |
            Measure-Object Length -Sum).Sum
    if (-not $sum) { return 0.0 }
    return [math]::Round($sum / 1MB, 2)
  } catch { return 0.0 }
}

$Root = (Resolve-Path $Root).Path
Set-Location $Root

$reportsDir = Join-Path $Root "outputs\reports"
Ensure-Dir $reportsDir

# Categories (adjust/add as needed)
$cats = @(
  @{Name='backups';    Path=(Join-Path $Root 'backups')},
  @{Name='quarantine'; Path=(Join-Path $Root 'quarantine')},
  @{Name='.git';       Path=(Join-Path $Root '.git')},
  @{Name='scripts';    Path=(Join-Path $Root 'scripts')},
  @{Name='outputs';    Path=(Join-Path $Root 'outputs')}
)

$report = @()
foreach ($c in $cats) {
  $mb = Get-FolderMB $c.Path
  $report += [pscustomobject]@{ Folder=$c.Name; SizeMB=$mb }
}
$total = [math]::Round(($report | Measure-Object SizeMB -Sum).Sum, 2)
$report += [pscustomobject]@{ Folder='TOTAL'; SizeMB=$total }

# Save TSV + JSON
$tsv  = Join-Path $reportsDir "space_audit.tsv"
$json = Join-Path $reportsDir "space_audit.json"
$report | Export-Csv -Delimiter "`t" -NoTypeInformation -Encoding UTF8 -Path $tsv
$report | ConvertTo-Json -Depth 4 | Out-File -Encoding UTF8 -FilePath $json

# Top-N largest files (for quick wins)
$largest = Get-ChildItem -Recurse -File -ErrorAction SilentlyContinue |
  Sort-Object Length -Descending |
  Select-Object -First $TopN `
    @{n='FullName';e={$_.FullName}},
    @{n='SizeMB'; e={[math]::Round($_.Length/1MB,2)}}

$largestTsv = Join-Path $reportsDir "space_audit_top${TopN}.tsv"
$largest | Export-Csv -Delimiter "`t" -NoTypeInformation -Encoding UTF8 -Path $largestTsv

Write-Host ""
Write-Host "MAGIC Space Audit @ $Root" -ForegroundColor Cyan
$report | Format-Table -AutoSize
Write-Host ""
Write-Host "Saved: $tsv"
Write-Host "Saved: $json"
Write-Host ("Saved: {0}" -f $largestTsv)
