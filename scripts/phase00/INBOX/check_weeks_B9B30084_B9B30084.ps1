# tools/gates/check_weeks.ps1  (minimal smoke check)
$ErrorActionPreference = "Stop"
$root   = (Resolve-Path "$PSScriptRoot\..\..").Path  # repo root
$outDir = Join-Path $root "outputs\reports"
New-Item -ItemType Directory -Force -Path $outDir | Out-Null
$stamp  = Get-Date -Format "yyyyMMdd_HHmmss"
$tsv    = Join-Path $outDir "week_status_report_$stamp.tsv"
$md     = Join-Path $outDir "week_status_report_$stamp.md"

function Row($Week,$Step,$Goal,$Check,$Result){[PSCustomObject]@{Week=$Week;Step=$Step;Goal=$Goal;Check=$Check;Result=$Result}}

$rows = @()
# Minimal evidence checks (expand later)
$rows += Row 1 '1.1' 'Inventory scripts'       'audit_list.txt'                 (Test-Path "$root\audit_list.txt")
$rows += Row 1 '1.2' 'Manifest generated'      'phase_manifest.json'            (Test-Path "$root\phase_manifest.json")
$rows += Row 2 '2.1' 'Logs emitted'            'outputs/logs/**/*.log'         ((Get-ChildItem "$root\outputs\logs" -Recurse -Filter *.log -ErrorAction SilentlyContinue).Count -gt 0)
$rows += Row 3 '3.4' 'Remediation in runner'   'apply_remediation in v5'       (Select-String "$root\self_healing_runner_v5.py" -Pattern 'apply_remediation' -Quiet -ErrorAction SilentlyContinue)
$rows += Row 4 '4.1' 'CI workflow present'     '.github/workflows/*.yml'       ((Get-ChildItem "$root\.github\workflows\*.yml" -ErrorAction SilentlyContinue).Count -gt 0)
$rows += Row 5 '5.2' 'Module B summary TSV'    'phase11/module_b/**/summary*.tsv' ((Get-ChildItem "$root\scripts\phase11\module_b" -Recurse -Filter 'summary*.tsv' -ErrorAction SilentlyContinue).Count -gt 0)
$rows += Row 6 '6.3' 'Parallel exec present'   'ProcessPoolExecutor in v5'     (Select-String "$root\self_healing_runner_v5.py" -Pattern 'ProcessPoolExecutor' -Quiet -ErrorAction SilentlyContinue)
$rows += Row 7 '7.3' 'Pytest in CI'            'pytest in workflow'            (Get-ChildItem "$root\.github\workflows\*.yml" | ForEach-Object { Select-String $_.FullName -Pattern 'pytest' -Quiet -ErrorAction SilentlyContinue } | Where-Object {$_} | Measure-Object | Select-Object -ExpandProperty Count)
$rows += Row 8 '8.1' 'Metrics emitted'         'metrics*.json'                  ((Get-ChildItem "$root\outputs" -Recurse -Filter 'metrics*.json' -ErrorAction SilentlyContinue).Count -gt 0)
$rows += Row 9 '9.1' 'Nightly all-phases log'  'outputs/nightly_allphases_*.log' ((Get-ChildItem "$root\outputs" -Filter 'nightly_allphases_*.log' -ErrorAction SilentlyContinue).Count -gt 0)
$rows += Row 10 '10.1' 'Backup tool exists'    'tools/backup_manifest.py'      (Test-Path "$root\tools\backup_manifest.py")
$rows += Row 11 '11.3' 'Auto patcher exists'   'tools/auto_patcher.py'         (Test-Path "$root\tools\auto_patcher.py")
$rows += Row 12 '12.2' 'Post-mortem exists'    'docs/post_mortem_report.md'    (Test-Path "$root\docs\post_mortem_report.md")

# Write TSV
$rows | Export-Csv -Delimiter "`t" -NoTypeInformation -Path $tsv

# Write MD (quick)
$mdText = "# Week Status (minimal) $stamp`n`n| Week | Step | Goal | Check | Result |`n|---|---|---|---|---|`n"
foreach($r in $rows){ $mdText += "| $($r.Week) | $($r.Step) | $($r.Goal) | $($r.Check) | " + ($(if($r.Result){"✅"} else {"❌"})) + " |`n" }
$mdText | Out-File -Encoding UTF8 $md

Write-Host "Saved:" -ForegroundColor Cyan
Write-Host " - TSV: $tsv"
Write-Host " - MD : $md"
