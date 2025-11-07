param([int]$Phase = 11)
$ErrorActionPreference = "Stop"

Write-Host "▶ Tests + coverage" -ForegroundColor Cyan
pytest

Write-Host "▶ Build dashboard (Phase $Phase)" -ForegroundColor Cyan
python tools/build_dashboard.py `
  --summary outputs/summaries/phase_master_summary.tsv `
  --metrics_glob "outputs/logs/agent_metrics/*.json" `
  --outdir outputs/dashboard `
  --restrict_phase $Phase

Write-Host "▶ E2E smoketest (Phase $Phase)" -ForegroundColor Cyan
python tools/e2e_smoketest.py --phase $Phase

Write-Host "✅ All good."
