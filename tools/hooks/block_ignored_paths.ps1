param([Parameter(ValueFromRemainingArguments=$true)][string[]]$Files)

$ErrorActionPreference = "Stop"

# Determine staged paths (prefer args from shim; otherwise diff)
$paths = @()
if ($Files -and $Files.Count -gt 0) {
  $paths = $Files | Where-Object { $_ -and $_.Trim() -ne "" }
} else {
  $paths = (git diff --cached --name-only) -split "`r?`n" | Where-Object { $_ -and $_.Trim() -ne "" }
}

# Block rules
$deny = @('^\.env$','^\.coverage$','^\.artifacts($|/|\\)')

$blocked = New-Object System.Collections.Generic.HashSet[string] ([StringComparer]::OrdinalIgnoreCase)
foreach ($p in $paths) {
  foreach ($re in $deny) { if ($p -match $re) { $null = $blocked.Add($p); break } }
}

if ($blocked.Count -gt 0) {
  Write-Host "🚫 Refusing to commit ignored/secret artifacts:" -ForegroundColor Red
  $blocked | Sort-Object | ForEach-Object {
    " - $_"
    Write-Output ("MAGIC_GUARD_BLOCK: {0}" -f $_)
  }
  exit 1
}

Write-Host "[OK] No forbidden files staged." -ForegroundColor Green
exit 0