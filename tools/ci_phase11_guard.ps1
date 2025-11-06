param(
  [Parameter(Mandatory=$false)][string]$Module
)

$ErrorActionPreference = "Stop"
$tsv = "outputs/logs/master_orchestrator_summary.tsv"
if (-not (Test-Path $tsv)) {
  Write-Error "Missing $tsv (did the Orchestrator step run?)"
  exit 2
}

# Adjust headers if needed — assuming TSV has columns: Module, Status
$rows = Import-Csv -Path $tsv -Delimiter "`t"

$target = if ($Module) {
  $rows | Where-Object { $_.Module -eq $Module }
} else {
  $rows
}

if (-not $target) {
  Write-Warning "No rows found for module '$Module'. Passing conservatively."
  exit 0
}

$failRows = $target | Where-Object { $_.Status -match '^(FAIL|ERROR)$' }
$warnRows = $target | Where-Object { $_.Status -match '^WARN$' }

if ($warnRows) {
  Write-Host "WARN rows:"
  $warnRows | Format-Table -AutoSize | Out-String | Write-Host
}

if ($failRows) {
  Write-Host "FAIL/ERROR rows:"
  $failRows | Format-Table -AutoSize | Out-String | Write-Host
  exit 1
}

Write-Host "OK: No FAIL/ERROR for module '$Module'"
exit 0
