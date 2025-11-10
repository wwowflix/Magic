Set-Location E:\MAGIC
$latest = Get-ChildItem .\outputs\reports\magic_full_status_scan_*.tsv |
  Sort-Object LastWriteTime | Select-Object -Last 1
python .\tools\scan\magic_import_fail_mark.py $latest.FullName .\outputs\reports\magic_full_status_scan_with_fail.tsv
python .\tools\status\summarize.py --in .\outputs\reports\magic_full_status_scan_with_fail.tsv --out .\outputs\reports\status_live_latest.tsv
python .\tools\scan\diag_fail_set.py
Get-Content .\outputs\reports\status_live_latest.tsv
