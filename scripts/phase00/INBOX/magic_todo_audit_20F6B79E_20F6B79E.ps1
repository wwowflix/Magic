param(
  [string]$Root = "."
)

$Reports = Join-Path $Root "outputs\reports"
New-Item -ItemType Directory -Force -Path $Reports | Out-Null

function Add-Row($w,$s,$what,$ok,$gapIfMissing) {
  $status = if ($ok) { "Done" } else { "Missing" }
  $gaps   = if ($ok) { "" } else { $gapIfMissing }
  [pscustomobject]@{ Week=$w; Step=$s; What=$what; Status=$status; Gaps=$gaps }
}

$rows = @()

# --- Week 4 ---
$rows += Add-Row 4 "4.3" "Alerts" (Test-Path "$Root\.github\workflows\self_heal.yml") ".github\workflows\self_heal.yml"

# --- Week 8 ---
$rows += Add-Row 8 "8.3" "Documentation" (Test-Path "$Root\docs\PRODUCTION_HANDOFF.md") "docs\PRODUCTION_HANDOFF.md"
$rows += Add-Row 8 "8.4" "Team demo" (Test-Path "$Root\docs\demos\week8_demo.md") "docs\demos\week8_demo.md"

# --- Week 9 ---
$rows += Add-Row 9 "9.1" "Stress test" (Test-Path "$Root\outputs\reports\stress_test_1000.tsv") "outputs\reports\stress_test_1000.tsv"
$rows += Add-Row 9 "9.2" "Optimize runner" ((Test-Path "$Root\outputs\reports\perf_profile.md") -and (Test-Path "$Root\outputs\reports\perf_delta.tsv")) "outputs\reports\perf_profile.md | outputs\reports\perf_delta.tsv"
$rows += Add-Row 9 "9.3" "Auto cleanup" ((Test-Path "$Root\tools\cleanup_agent.py") -and (Test-Path "$Root\outputs\reports\cleanup_last_run.txt")) "tools\cleanup_agent.py | outputs\reports\cleanup_last_run.txt"
$rows += Add-Row 9 "9.4" "Notion sync" ((Test-Path "$Root\tools\notion_sync_agent.py") -and (Test-Path "$Root\outputs\logs\notion_sync\last_sync.txt")) "tools\notion_sync_agent.py | outputs\logs\notion_sync\last_sync.txt"
$rows += Add-Row 9 "9.5" "Scale-prep PR merged" (Test-Path "$Root\outputs\reports\PR_scale_prep_MERGED.txt") "outputs\reports\PR_scale_prep_MERGED.txt"

# --- Week 10 ---
$rows += Add-Row 10 "10.2" "Auto-recover failures" (Test-Path "$Root\outputs\reports\retry_queue_receipt.txt") "outputs\reports\retry_queue_receipt.txt"
$rows += Add-Row 10 "10.3" "Self-repair bot" (Test-Path "$Root\docs\flows\self_repair_flow.json") "docs\flows\self_repair_flow.json"
$rows += Add-Row 10 "10.4" "Disaster simulation" (Test-Path "$Root\docs\reports\chaos_test_report.md") "docs\reports\chaos_test_report.md"
$rows += Add-Row 10 "10.5" "Failover PR merged" (Test-Path "$Root\outputs\reports\PR_failover_MERGED.txt") "outputs\reports\PR_failover_MERGED.txt"

# --- Week 11 ---
$rows += Add-Row 11 "11.1" "AI remediation" ((Test-Path "$Root\tools\apply_remediation_ai.py") -and (Test-Path "$Root\outputs\reports\ai_remediation_log.txt")) "tools\apply_remediation_ai.py | outputs\reports\ai_remediation_log.txt"
$rows += Add-Row 11 "11.2" "Smart prioritization" (Test-Path "$Root\outputs\reports\priority_order.tsv") "outputs\reports\priority_order.tsv"
$rows += Add-Row 11 "11.4" "Notion/GitHub alerts" (Test-Path "$Root\outputs\reports\alerts_last.txt") "outputs\reports\alerts_last.txt"

# --- Week 12 ---
$tagList = & git tag --list v1.0-stable 2>$null
$hasTag  = ($tagList -and $tagList.Trim() -ne "")
$rows += Add-Row 12 "12.3" "Freeze version" ($hasTag -or (Test-Path "$Root\outputs\reports\TAG_v1.0-stable_OK.txt")) "git tag v1.0-stable OR outputs\reports\TAG_v1.0-stable_OK.txt"
$rows += Add-Row 12 "12.4" "Ops handoff" (Test-Path "$Root\docs\demos\ops_handoff.md") "docs\demos\ops_handoff.md"

# Output table
$flat = $rows | Sort-Object Week, Step
$flat | Format-Table -AutoSize

# Save TSV
$tsvPath = Join-Path $Reports "magic_todo_audit.tsv"
$flat | Export-Csv -Delimiter "`t" -NoTypeInformation -Encoding UTF8 -Path $tsvPath

# Save Markdown
$mdPath  = Join-Path $Reports "magic_todo_audit.md"
$md = @("# MAGIC - To-Do Audit","","| Week | Step | What | Status | Gaps |","|-----:|------|------|--------|------|")
foreach ($r in $flat) {
  $md += ("| {0} | {1} | {2} | {3} | {4} |" -f $r.Week, $r.Step, ($r.What -replace '\|','\|'), $r.Status, (($r.Gaps -replace '\|','\|') -replace '\r?\n',' '))
}
($md -join "`r`n") | Out-File -Encoding UTF8 -FilePath $mdPath

Write-Host "`nSaved:`n - $tsvPath`n - $mdPath"
