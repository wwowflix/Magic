# MAGIC signing guard (stub) — customize to your policy
# Blocks push if a GPG signing env var is missing; exit 0 to relax policy.
if (-not $env:GIT_COMMITTER_SIGNINGKEY) {
  Write-Host "WARN: No signing key env set (GIT_COMMITTER_SIGNINGKEY)" -ForegroundColor Yellow
  exit 0
}
exit 0
