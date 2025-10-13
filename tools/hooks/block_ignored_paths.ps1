# tools/hooks/block_ignored_paths.ps1
$ErrorActionPreference = "Stop"

# Get staged paths (NUL-separated to handle weird names)
$staged = git diff --cached --name-only -z
$paths  = -split ($staged -as [string]), "`0" | Where-Object { $_ -ne "" }

# Patterns to block (repo-root relative)
$deny = @(
  '^\.env$',
  '^\.coverage$',
  '^\.artifacts($|/|\\)'
)

$blocked = @()
foreach($p in $paths){
  foreach($re in $deny){
    if($p -match $re){ $blocked += $p; break }
  }
}

if($blocked.Count -gt 0){
  Write-Host "[BLOCK] Commit blocked by guard. Remove these from the index:" -ForegroundColor Red
  $blocked | Sort-Object -Unique | ForEach-Object { " - $_" }
  exit 1
}

Write-Host "[OK] No forbidden files staged." -ForegroundColor Green
exit 0