[CmdletBinding()]
param(
  [string]$Root = (Resolve-Path ".").Path
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$forbidden = Join-Path $Root 'outputs\reports\status\guard_test.txt'
New-Item -ItemType Directory -Force -Path (Split-Path $forbidden) | Out-Null
'test' | Set-Content $forbidden

git -C $Root add -f $forbidden | Out-Null

try {
  git -C $Root commit -m "guard self-test" | Out-Null
  throw "❌ Guard did NOT block commit"
} catch {
  Write-Host "✅ Pre-commit guard blocked as expected." -ForegroundColor Green
} finally {
  git -C $Root reset HEAD -- $forbidden | Out-Null
  Remove-Item $forbidden -Force -ErrorAction SilentlyContinue
}
