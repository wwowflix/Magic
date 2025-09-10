[CmdletBinding()]
param()
$ErrorActionPreference = "Stop"
$Root    = "D:\MAGIC"
$Reports = Join-Path $Root "outputs\reports"
$Backups = Join-Path $Root "outputs\backups"
$null = New-Item -ItemType Directory -Force -Path $Reports | Out-Null
$Py = Join-Path $Root "venv\Scripts\python.exe"
if (-not (Test-Path $Py)) { try { $Py = (Get-Command py -ErrorAction Stop).Source } catch { $Py = (Get-Command python -ErrorAction Stop).Source } }
$env:PYTHONWARNINGS = "ignore"

# compile helper (optional)
$Help = Join-Path $Root "tmp\compile_ready_helper.py"
$rep = $null
if (Test-Path $Help) { try { $rep = (& $Py -W ignore $Help 2>$null) | ConvertFrom-Json } catch { $rep = $null } }
if (-not $rep) { $rep = [pscustomobject]@{ total=0; failed=0; fails=@() } }

# ensure 11D data exists
$depsJson = Join-Path $Reports "deps_graph.json"
$orphTsv  = Join-Path $Reports "orphans_by_dir.tsv"
$D11 = Join-Path $Root "scripts\phase11\module_D\11D_dependency_orphan_audit_READY.py"
if (-not (Test-Path $depsJson) -or -not (Test-Path $orphTsv)) { if (Test-Path $D11) { try { & $Py -W ignore $D11 2>$null | Out-Null } catch {} } }
$deps = if (Test-Path $depsJson) { Get-Content $depsJson | ConvertFrom-Json } else { [pscustomobject]@{ inbound=@{}; orphans=@() } }

# metrics
$today = (Get-Date).Date
$healed=0;$quarantined=0;$stubbed=0
if (Test-Path $Backups) {
  $indentDirs = Get-ChildItem $Backups -Directory -Filter "indentfix_*" -ErrorAction SilentlyContinue | Where-Object { $_.LastWriteTime.Date -eq $today }
  if ($indentDirs) { $healed = ($indentDirs | ForEach-Object { Get-ChildItem -Recurse $_.FullName -File -Include *.py } | Measure-Object).Count }
  $stubbed = (Get-ChildItem $Backups -Directory -Filter "stubs_*" -ErrorAction SilentlyContinue | Where-Object { $_.LastWriteTime.Date -eq $today } | ForEach-Object { Get-ChildItem -Recurse $_.FullName -File } | Measure-Object).Count
}
$qr = Join-Path $Root "quarantine\compile_fail"
if (Test-Path $qr) { $quarantined = (Get-ChildItem -Recurse $qr -File -ErrorAction SilentlyContinue | Where-Object { $_.LastWriteTime.Date -eq $today } | Measure-Object).Count }

# summary TSV
$tsv = Join-Path $Reports "compile_summary.tsv"
@"
metric`tvalue
remaining_fails`t$($rep.failed)
orphans_total`t$($deps.orphans.Count)
healed_in_indentfix`t$healed
quarantined_today`t$quarantined
stubbed_today`t$stubbed
"@ | Set-Content -LiteralPath $tsv -Encoding UTF8

# history (dedupe-per-day)
$hist = Join-Path $Reports "week11_history.tsv"
if (-not (Test-Path $hist)) { "date`tremaining_fails`torphans_total`thealed_in_indentfix`tquarantined_today`tstubbed_today" | Set-Content -LiteralPath $hist -Encoding UTF8 }
("{0:yyyy-MM-dd}`t{1}`t{2}`t{3}`t{4}`t{5}" -f (Get-Date), $rep.failed, $deps.orphans.Count, $healed, $quarantined, $stubbed) | Add-Content -LiteralPath $hist -Encoding UTF8
$rows = Import-Csv -Delimiter "`t" $hist
$rows = $rows | Group-Object date | ForEach-Object { $_.Group[-1] }
$rows | Export-Csv -Delimiter "`t" -NoTypeInformation -Encoding UTF8 $hist

# markdown
$md = Join-Path $Reports "week11_audit.md"
$top = @(); if (Test-Path $orphTsv) { $top = Import-Csv -Delimiter "`t" $orphTsv | Select-Object -First 10 }
$lines = @()
$lines += "# Week 11 Audit","",("**Date:** {0}" -f (Get-Date -Format "yyyy-MM-dd HH:mm:ss")),"","## Summary","",
"| Metric | Value |","|---|---:|",
("| Remaining fails | {0} |" -f $rep.failed),
("| Orphans (11D) | {0} |" -f $deps.orphans.Count),
("| Healed in indentfix (today) | {0} |" -f $healed),
("| Quarantined (today) | {0} |" -f $quarantined),
("| Stubbed (today) | {0} |" -f $stubbed),"","Artifacts:"
@(
  (Join-Path $Reports "compile_summary.tsv"),
  (Join-Path $Reports "compile_error_buckets.tsv"),
  (Join-Path $Reports "compile_error_buckets.json"),
  (Join-Path $Reports "deps_graph.json"),
  (Join-Path $Reports "orphans_by_dir.tsv"),
  (Join-Path $Reports "orphan_lib_review.tsv")
) | ForEach-Object { $lines += ("- ``{0}``" -f $_) }
$lines += "","## Top orphan directories","","| Folder | Orphans |","|---|---:|"
$top | ForEach-Object { $lines += ("| {0} | {1} |" -f $_.folder, $_.orphans) }
$lines -join "`r`n" | Set-Content -LiteralPath $md -Encoding UTF8

"wrap: fails=$($rep.failed) orphans=$($deps.orphans.Count) healed=$healed quarantined=$quarantined stubbed=$stubbed" | Write-Host
"wrote: $tsv`n       $hist`n       $md" | Write-Host
