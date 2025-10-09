param(
  [string]$Table = ".\outputs\reports\readiness\status_live_latest.tsv",
  [string[]]$Actions = @(),          # exact matches
  [string[]]$ActionsLike = @(),      # wildcards, e.g. '*Docker build*'
  [ValidateSet('✅ Done','✅ Done (N/A on this machine)','⏳ In Progress','⏭ Not Started')]
  [string]$Status = '✅ Done'
)

if (-not (Test-Path $Table)) { throw "Table not found: $Table" }
$rows = Import-Csv -Delimiter "`t" $Table
$changed = 0
foreach ($r in $rows) {
  $act = [string]$r.'Action (PowerShell / Command)'
  $matchExact = $Actions -contains $act
  $matchLike  = $false
  foreach ($p in $ActionsLike) { if ($act -like $p) { $matchLike = $true; break } }

  if ($matchExact -or $matchLike) {
    if ($r.Status -ne $Status) { $r.Status = $Status; $changed++ }
  }
}
$rows | Export-Csv -Delimiter "`t" -NoTypeInformation -Encoding UTF8 $Table
Write-Host "Updated $changed row(s) → $Table" -ForegroundColor Green
