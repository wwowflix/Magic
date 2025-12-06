# MAGIC Week 1 – Spine Runner (W1D3-3)
# Runs all Week-1 smoketests together as a single sanity check.

Set-StrictMode -Version Latest
Set-Location E:\MAGIC

Write-Host ""
Write-Host "===== MAGIC Week 1 – Spine Runner (W1D3-3) =====" -ForegroundColor Cyan
Write-Host "Running all Week-1 smoketests..." -ForegroundColor Cyan

$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD = "1"

$tests = $tests = @(
  # Data flows
  "tests/smoke/test_data_smoke.py",
  "tests/smoke/test_data_generated_smoke.py",

  # AI flows
  "tests/smoke/test_ai_flow_mvp.py",
  "tests/smoke/test_ai_generated_smoke.py",

  # Registry + manifest
  "tests/smoke/test_flow_registry.py",
  "tests/smoke/test_flow_manifest.py",

  # Error flows (new)
  "tests/smoke/test_error_flow_mvp.py",
  "tests/smoke/test_error_template_smoke.py",
  "tests/smoke/test_error_generated_smoke.py"
)


$pytestArgs = @()
$pytestArgs += $tests
$pytestArgs += "-q"

Write-Host ""
Write-Host ">>> Running:" ($pytestArgs -join " ") "`n"

pytest @pytestArgs
$exit = $LASTEXITCODE

Write-Host ""

if ($exit -eq 0) {
    Write-Host ">>> Week-1 Spine Runner PASSED — all smoketests green. " -ForegroundColor Green
    exit 0
}
else {
    Write-Host ">>> Week-1 Spine Runner FAILED — see failure above. " -ForegroundColor Red
    exit $exit
}
