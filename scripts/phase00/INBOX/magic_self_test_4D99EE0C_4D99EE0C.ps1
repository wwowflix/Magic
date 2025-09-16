[CmdletBinding()]
param(
  [string]$Root = "D:\MAGIC",
  [int]$LargeMB = 200,
  [int]$OldDays = 120,
  [int]$HashMaxMB = 1024
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Join-PathSafe([string]$a,[string]$b){ Join-Path -Path $a -ChildPath $b }

# Run scan
powershell -NoProfile -ExecutionPolicy Bypass `
  -File (Join-PathSafe $Root "tools\magic_full_scan.ps1") `
  -Root $Root -LargeMB $LargeMB -OldDays $OldDays -HashMaxMB $HashMaxMB `
  -IncludeGit:$false -IncludeVenv:$false

$rep = Join-PathSafe $Root "outputs\reports\scan"
$invPath = Join-PathSafe $rep "inventory_full.tsv"
$largeP  = Join-PathSafe $rep "large_files.tsv"
$oldP    = Join-PathSafe $rep "old_files.tsv"
$dupsP   = Join-PathSafe $rep "duplicates_by_hash.tsv"
$orphP   = Join-PathSafe $rep "orphans.tsv"

# Quick counts
function Count-Lines($p){ if(Test-Path $p){ (Get-Content $p -TotalCount 999999 | Measure-Object -Line).Lines - 1 } else { 0 } }

$largeN = Count-Lines $largeP
$oldN   = Count-Lines $oldP
$dupsN  = Count-Lines $dupsP
$orphN  = Count-Lines $orphP

Write-Host "=== SELF-TEST SUMMARY ==="
Write-Host ("Large(≥{0}MB): {1}" -f $LargeMB,$largeN)
Write-Host ("Old(≥{0}d):   {1}" -f $OldDays,$oldN)
Write-Host ("Duplicates:    {0}" -f $dupsN)
Write-Host ("Orphans:       {0}" -f $orphN)

$hasWarn = ($largeN -gt 0) -or ($oldN -gt 0) -or ($dupsN -gt 0) -or ($orphN -gt 0)
if ($hasWarn){ exit 2 } else { exit 0 }
