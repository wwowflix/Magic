param(
  [switch]$DryRun
)

$root = (git rev-parse --show-toplevel).Trim()
Set-Location $root

$targets = @(
  "tools/reports/*",
  "smoke_*.txt",
  "smoke_last_run.txt",
  "smoke_failed_tests.txt",
  "probe_*.py",
  "missing_modules.txt"
)

Write-Host "MAGIC cleanup running in: $root"
Write-Host "DryRun: $DryRun"

foreach ($t in $targets) {
  if ($DryRun) {
    Get-ChildItem -Path $t -ErrorAction SilentlyContinue | ForEach-Object {
      Write-Host "Would remove $($_.FullName)"
    }
  } else {
    Remove-Item -Force -Recurse $t -ErrorAction SilentlyContinue
  }
}

Write-Host "Done."
