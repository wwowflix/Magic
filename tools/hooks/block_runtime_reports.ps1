param(
  [string]$RepoRoot = $(git rev-parse --show-toplevel 2>$null)
)

if ($env:SKIP_RUNTIME_GUARD -eq '1') {
  Write-Host "[block-runtime-reports] SKIP_RUNTIME_GUARD=1 set, skipping checks."
  exit 0
}

if (-not $RepoRoot) {
  Write-Host "[block-runtime-reports] Not in a git repo, skipping."
  exit 0
}

$raw = git -C $RepoRoot diff --cached --name-only -z --diff-filter=AM 2>$null
if (-not $raw) {
  exit 0
}

$staged = ($raw -split "`0") | Where-Object { $_ -and $_.Trim() -ne "" }
$staged = $staged | ForEach-Object { $_ -replace '\\','/' }

$dirPrefixes = @(
  'outputs/reports/readiness/',
  'outputs/reports/status/',
  'outputs/reports/tests/',
  'outputs/reports/ci/',
  'outputs/reports/env/',
  'outputs/reports/coverage/'
)

$filePrefixes = @(
  'outputs/reports/status_now.'
)

$violations = New-Object System.Collections.Generic.List[string]

foreach ($f in $staged) {
  $blockedDir  = $false
  $blockedFile = $false

  foreach ($d in $dirPrefixes) {
    if ($f.StartsWith($d, [System.StringComparison]::OrdinalIgnoreCase)) {
      $blockedDir = $true; break
    }
  }
  if (-not $blockedDir) {
    foreach ($p in $filePrefixes) {
      if ($f.StartsWith($p, [System.StringComparison]::OrdinalIgnoreCase)) {
        $blockedFile = $true; break
      }
    }
  }

  if ($blockedDir -or $blockedFile) {
    $violations.Add($f) | Out-Null
  }
}

if ($violations.Count -gt 0) {
  Write-Host ""
  Write-Host "❌ The following staged paths are runtime reports and must not be committed:" -ForegroundColor Red
  $violations | ForEach-Object { Write-Host "  - $_" -ForegroundColor Yellow }
  Write-Host ""
  Write-Host "To fix: unstage them, e.g.:" -ForegroundColor Cyan
  Write-Host "  git reset HEAD -- <path>" -ForegroundColor Cyan
  Write-Host ""
  Write-Host "If you *really* must bypass this (discouraged), temporarily:" -ForegroundColor DarkYellow
  Write-Host "  `$Env:SKIP_RUNTIME_GUARD = '1'  # then commit" -ForegroundColor DarkYellow
  exit 1
}

exit 0
