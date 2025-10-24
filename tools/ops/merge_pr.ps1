[CmdletBinding()]
param(
  [int]$PR,
  [ValidateSet('squash','merge','rebase')]
  [string]$Method = 'squash',
  [switch]$NoWatch,
  [switch]$Auto
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

function Get-PRNumberFromBranch {
  $branch = git rev-parse --abbrev-ref HEAD
  if (-not $branch) { return $null }
  if ($branch -eq 'main' -or $branch -eq 'origin/main') { return $null }
  try {
    $num = gh pr list -H $branch --json number --jq '.[0].number' 2>$null
    return $num
  } catch {
    return $null
  }
}

# Resolve PR number
if (-not $PR) {
  $PR = Get-PRNumberFromBranch
  if (-not $PR) {
    Write-Host "No PR number supplied and no PR associated with current branch. Use -PR <number>." -ForegroundColor Yellow
    exit 2
  }
}

Write-Host "Using PR #$PR" -ForegroundColor Cyan

# Optional check watching
try {
  if ($NoWatch) {
    gh pr checks $PR
  } else {
    gh pr checks $PR --watch
  }
} catch {
  Write-Host "Warning: could not fetch/check PR checks: $($_.Exception.Message)" -ForegroundColor Yellow
}

# Merge method
$mergeArgs = @('pr','merge',"$PR","--$Method")
if ($Auto) { $mergeArgs += '--auto' }

# Execute merge
try {
  & gh @mergeArgs
} catch {
  Write-Host "Merge failed: $($_.Exception.Message)" -ForegroundColor Red
  exit 1
}
