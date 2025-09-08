param(
  [Parameter(Mandatory=$true)][string]$Message,
  [switch]$NoVerify,
  [switch]$NoPush
)

$ErrorActionPreference = 'Stop'

function Assert-GitReady {
  if (-not (Get-Command git -ErrorAction SilentlyContinue)) { throw "git not found in PATH." }
  $null = git rev-parse --is-inside-work-tree 2>$null
  if ($LASTEXITCODE -ne 0) { throw "Not inside a git repository." }
}
Assert-GitReady

# 1) Stage only tracked modifications/deletions
git add -u

Write-Host "`nStaged changes:" -ForegroundColor Cyan
$staged = git diff --cached --name-status
if (-not $staged) {
  Write-Host "Nothing to commit (only tracked files are considered).`n" -ForegroundColor Yellow
  exit 0
}
$staged | Write-Host

# 2) Commit
$commitArgs = @("-m", $Message)
if ($NoVerify) { $commitArgs += "--no-verify" }
git commit @commitArgs

# 3) Push
if (-not $NoPush) {
  git push
  if ($LASTEXITCODE -ne 0) { throw "Push failed." }
}

Write-Host "`n✅ Done." -ForegroundColor Green
