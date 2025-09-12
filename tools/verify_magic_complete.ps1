$ErrorActionPreference = "Stop"
$Root = "D:\MAGIC"
Set-Location $Root

function Ok($m){ Write-Host "OK   $m" -ForegroundColor Green }
function No($m){ Write-Host "FAIL $m" -ForegroundColor Red; $script:hadFail = $true }
$hadFail = $false

$Reports   = Join-Path $Root "outputs\reports"
$DashIndex = Join-Path $Root "outputs\dashboard\index.html"

Write-Host "`n=== MAGIC – Final Verification ===`n" -ForegroundColor Cyan

# 1) Rebuild scan + assert Week 12 Done
try{
  powershell -NoProfile -ExecutionPolicy Bypass -File (Join-Path $Root "tools\magic_scan_status.ps1") -Root $Root | Out-Null
  $scan = Get-Content (Join-Path $Reports "magic_scan_summary.json") -Raw | ConvertFrom-Json
  $w = $scan.weeks | Where-Object { $_.Status -eq "Done" } | Sort-Object Week | Select-Object -Last 1
  if($w.Week -eq 12 -and $w.Status -eq "Done"){ Ok "Week $($w.Week) — $($w.Step) — $($w.Status)" } else { No "Not at Week 12/Done" }
}catch{ No "magic_scan_status.ps1 failed: $($_.Exception.Message)" }

# 2) To-Do audit must have zero Missing
try{
  powershell -NoProfile -ExecutionPolicy Bypass -File (Join-Path $Root "tools\magic_todo_audit.ps1") -Root $Root | Out-Null
  $audit = Import-Csv -Delimiter "`t" (Join-Path $Reports "magic_todo_audit.tsv")
  $missing = $audit | Where-Object { $_.Status -ne "Done" }
  if(($missing | Measure-Object).Count -eq 0){ Ok "To-Do audit: 0 Missing" } else { No "Audit has Missing items" }
}catch{ No "magic_todo_audit.ps1 failed: $($_.Exception.Message)" }

# 3) Receipts (prove the tricky gaps)
$must = @(
  ".github\workflows\self_heal.yml",
  "docs\demos\week8_demo.md",
  "outputs\dashboard\index.html",
  "outputs\reports\stress_test_1000.tsv",
  "outputs\reports\perf_profile.md",
  "outputs\reports\perf_delta.tsv",
  "tools\cleanup_agent.py",
  "outputs\reports\cleanup_last_run.txt",
  "tools\notion_sync_agent.py",
  "outputs\logs\notion_sync\last_sync.txt",
  "outputs\reports\PR_scale_prep_MERGED.txt",
  "outputs\reports\retry_queue_receipt.txt",
  "docs\flows\self_repair_flow.json",
  "docs\flows\self_repair_flow.png",
  "docs\reports\chaos_test_report.md",
  "outputs\reports\PR_failover_MERGED.txt",
  "tools\apply_remediation_ai.py",
  "outputs\reports\ai_remediation_log.txt",
  "outputs\reports\priority_order.tsv",
  "outputs\reports\alerts_last.txt",
  "docs\PRODUCTION_HANDOFF.md",
  "docs\demos\ops_handoff.md"
) | ForEach-Object { Join-Path $Root $_ }

$miss = $must | Where-Object { -not (Test-Path $_) }
if(($miss | Measure-Object).Count -eq 0){ Ok "All expected receipts exist ($($must.Count))" } else { $miss | ForEach-Object { Write-Host "  - $_" }; No "Missing receipt files: $($miss.Count)" }

# 4) Matplotlib import
try{
  & "$Root\venv\Scripts\python.exe" -c "import importlib; importlib.import_module('matplotlib'); print('matplotlib OK')"
  Ok "matplotlib import OK"
}catch{ No "matplotlib import failed: $($_.Exception.Message)" }

# 5) Pytest smoke
try{
  & "$Root\venv\Scripts\pytest.exe" -q | Out-Null
  Ok "pytest suite passes"
}catch{ No "pytest failed: $($_.Exception.Message)" }

# 6) Tag present locally and remote
try{
  $local  = git tag --list v1.0-stable
  $remote = git ls-remote --tags origin v1.0-stable
  if($local -and $remote){ Ok "Git tag v1.0-stable present (local + origin)" } else { No "Git tag v1.0-stable missing" }
}catch{ No "Git tag check failed: $($_.Exception.Message)" }

# 7) Dashboard index exists
if(Test-Path $DashIndex){ Ok "Dashboard index exists" } else { No "Dashboard index missing" }

Write-Host ""
if($hadFail){ Write-Host "FINAL: ❌ NOT COMPLETE" -ForegroundColor Red; exit 1 }
else{ Write-Host "FINAL: ✅ ALL WEEKS COMPLETE" -ForegroundColor Green; exit 0 }
