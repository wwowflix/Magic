param(
  [string]$Version = "v1.0.0-rc1"  # change if needed
)

$ErrorActionPreference = 'Stop'

function Step($name, [scriptblock]$b) {
  Write-Host (">> " + $name) -ForegroundColor Cyan
  & $b
  if ($LASTEXITCODE -ne 0) {
    throw "$name failed with exit code $LASTEXITCODE"
  }
  Write-Host ("OK " + $name) -ForegroundColor Green
}

$OUT = "outputs\reports\readiness"
New-Item -ItemType Directory -Force -Path $OUT | Out-Null

Step "Pre-commit hooks"          { pre-commit run --all-files }
Step "Unit tests"                { pytest -q }
Step "Coverage >= 75%"           { pytest --cov=./ --cov-fail-under=75 }
Step "pip-audit"                 { pip-audit -r requirements.txt }
Step "Safety check"              { safety check -r requirements.txt }
Step "Bandit (security)"         { bandit -q -r scripts }

# Minimal build artifacts placeholder (customize for your project)
Step "Build artifacts (stub)"    {
  $art = "outputs\artifacts"
  New-Item -ItemType Directory -Force -Path $art | Out-Null
  if (Test-Path ".pre-commit-config.yaml") { Copy-Item ".pre-commit-config.yaml" "$art\pre-commit-config.yaml" -Force }
  if (Test-Path ".gitattributes")          { Copy-Item ".gitattributes"          "$art\.gitattributes"          -Force }
  if (Test-Path "pyproject.toml")          { Copy-Item "pyproject.toml"          "$art\pyproject.toml"          -Force }
}

# Snapshot report (TSV)
$tsv  = Join-Path $OUT "production_readiness.tsv"
$rows = @(
  "Check`tResult",
  "pre-commit`tPASS",
  "pytest`tPASS",
  "coverage>=75%`tPASS",
  "pip-audit`tPASS",
  "safety`tPASS",
  "bandit`tPASS"
)
$rows | Set-Content -Encoding UTF8 $tsv

Write-Host "All checks passed. Preparing RC tag and PR hints..." -ForegroundColor Green

# Tag (local). Push manually to keep control.
git tag -f $Version
Write-Host ("Created tag " + $Version + " (local). Push with: git push -f origin " + $Version) -ForegroundColor Yellow

# Compute branch for display (avoid $(...) inside strings)
$branch = (git rev-parse --abbrev-ref HEAD).Trim()

Write-Host ""
Write-Host "Next steps:" -ForegroundColor Magenta
Write-Host ("  1) git push -u origin " + $branch) -ForegroundColor Magenta
Write-Host ("  2) gh pr create --base main --head " + $branch + " --title ""Prod: " + $Version + """ --body ""All gates passed; artifacts ready.""") -ForegroundColor Magenta
Write-Host ("  3) git push -f origin " + $Version) -ForegroundColor Magenta