param([Parameter(ValueFromRemainingArguments=$true)][string[]]$Files)

$ErrorActionPreference = "Stop"

# Prefer filenames from pre-commit args; fallback to staged diff
$paths = @()
if ($Files -and $Files.Count -gt 0) {
  $paths = $Files | Where-Object { $_ -and $_.Trim() -ne "" }
} else {
  $paths = (& git diff --cached --name-only) -split "`r?`n" | Where-Object { $_ -and $_.Trim() -ne "" }
}

# Block rules
$deny = @('^\.env$','^\.coverage$','^\.artifacts($|/|\\)')

$blocked = New-Object System.Collections.Generic.HashSet[string] ([StringComparer]::OrdinalIgnoreCase)
foreach ($p in $paths) {
  foreach ($re in $deny) { if ($p -match $re) { $null = $blocked.Add($p); break } }
}

if ($blocked.Count -gt 0) {
  Write-Host "[BLOCK] Commit blocked by guard. Remove these from the index:" -ForegroundColor Red
  $blocked | Sort-Object | ForEach-Object {
    " - param([Parameter(ValueFromRemainingArguments=$true)][string[]]$Files)

$ErrorActionPreference = "Stop"

# Prefer filenames from pre-commit args; fallback to staged diff
$paths = @()
if ($Files -and $Files.Count -gt 0) {
  $paths = $Files | Where-Object { $_ -and $_.Trim() -ne "" }
} else {
  $paths = (& git diff --cached --name-only) -split "`r?`n" | Where-Object { $_ -and $_.Trim() -ne "" }
}

# Block rules
$deny = @('^\.env$','^\.coverage$','^\.artifacts($|/|\\)')

$blocked = New-Object System.Collections.Generic.HashSet[string] ([StringComparer]::OrdinalIgnoreCase)
foreach ($p in $paths) {
  foreach ($re in $deny) { if ($p -match $re) { $null = $blocked.Add($p); break } }
}

if ($blocked.Count -gt 0) {
  Write-Host "[BLOCK] Commit blocked by guard. Remove these from the index:" -ForegroundColor Red
  $blocked | Sort-Object | ForEach-Object { " - $_" }
  exit 1
}

Write-Host "[OK] No forbidden files staged." -ForegroundColor Green
exit 0"
    # stable, machine-readable marker per blocked path:
    Write-Output ("MAGIC_GUARD_BLOCK: {0}" -f param([Parameter(ValueFromRemainingArguments=$true)][string[]]$Files)

$ErrorActionPreference = "Stop"

# Prefer filenames from pre-commit args; fallback to staged diff
$paths = @()
if ($Files -and $Files.Count -gt 0) {
  $paths = $Files | Where-Object { $_ -and $_.Trim() -ne "" }
} else {
  $paths = (& git diff --cached --name-only) -split "`r?`n" | Where-Object { $_ -and $_.Trim() -ne "" }
}

# Block rules
$deny = @('^\.env$','^\.coverage$','^\.artifacts($|/|\\)')

$blocked = New-Object System.Collections.Generic.HashSet[string] ([StringComparer]::OrdinalIgnoreCase)
foreach ($p in $paths) {
  foreach ($re in $deny) { if ($p -match $re) { $null = $blocked.Add($p); break } }
}

if ($blocked.Count -gt 0) {
  Write-Host "[BLOCK] Commit blocked by guard. Remove these from the index:" -ForegroundColor Red
  $blocked | Sort-Object | ForEach-Object { " - $_" }
  exit 1
}

Write-Host "[OK] No forbidden files staged." -ForegroundColor Green
exit 0)
  }
  exit 1
}

Write-Host "[OK] No forbidden files staged." -ForegroundColor Green
exit 0