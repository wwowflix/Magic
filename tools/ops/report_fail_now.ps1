Set-Location E:\MAGIC

$latest = Get-ChildItem .\outputs\reports\magic_full_status_scan_*.tsv |
  Sort-Object LastWriteTime | Select-Object -Last 1

python .\tools\scan\magic_import_fail_mark.py $latest.FullName .\outputs\reports\magic_full_status_scan_with_fail.tsv
python .\tools\status\summarize.py --in .\outputs\reports\magic_full_status_scan_with_fail.tsv --out .\outputs\reports\status_live_latest.tsv
python .\tools\scan\diag_fail_set.py

$diag = Import-Csv .\outputs\reports\magic_fail_diag_latest.tsv -Delimiter "`t"
$summary = $diag | Group-Object diag_type | Sort-Object Count -Descending
$ts = Get-Date -Format "yyyyMMdd_HHmmss"

$summary | Export-Csv ".\outputs\reports\fail_summary_$ts.tsv" -NoTypeInformation -Delimiter "`t"

@"
# MAGIC Fail Report – $ts

**Total Failed Files:** $($diag.Count)

| Error Type | Count |
|-------------|--------|
$(
  $summary | ForEach-Object {
    "| $($_.Name) | $($_.Count) |"
  } | Out-String
)
"@ | Set-Content -Encoding UTF8 ".\outputs\reports\fail_summary_$ts.md"

Write-Host "Report written to outputs\reports\fail_summary_$ts.md"
Get-Content .\outputs\reports\status_live_latest.tsv
