param(
  [string]$Root = "D:\MAGIC",
  [int]$RecentDays = 7
)
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function J([string]$p){ Join-Path $Root $p }
function Row([string]$cat,[string]$name,[object]$val,[string]$st,[string]$notes=""){
  [pscustomobject]@{ category=$cat; name=$name; value=$val; status=$st; notes=$notes }
}

$rows   = [System.Collections.Generic.List[object]]::new()
$errors = [System.Collections.Generic.List[string]]::new()
$tsNow  = Get-Date

# Ensure reports dir
$reportsDir = J "outputs\reports"
if(!(Test-Path $reportsDir)){ New-Item -ItemType Directory -Force -Path $reportsDir | Out-Null }

# Basic repo checks
$rows.Add((Row "repo" "root_path" $Root "INFO"))
$hasGit = Test-Path (J ".git")
$rows.Add((Row "repo" "has_git" $hasGit ($(if($hasGit){"PASS"}else{"FAIL"}))))

# Python venv
$venv = Test-Path (J "venv")
$rows.Add((Row "python" "venv_exists" $venv ($(if($venv){"PASS"}else{"FAIL"}))))

# pre-commit hook present?
$hookInstalled = Test-Path (J ".git\hooks\pre-commit")
$rows.Add((Row "hooks" "pre-commit" $hookInstalled ($(if($hookInstalled){"PASS"}else{"WARN"})) "hook file present"))

# Required receipt presence
$req = @{
  sbom           = "outputs\reports\sbom.json"
  sli            = "outputs\reports\sli_metrics.json"
  commit_receipt = "outputs\reports\commit_receipt.txt"
  magic_scan_json= "outputs\reports\magic_complete_scan.json"
  restore_probe  = "outputs\reports\restore_probe_receipt.txt"
  slo            = "outputs\reports\slo_enforce.json"
  offsite_backup = "outputs\reports\offsite_backup_receipt.txt"
  magic_scan_tsv = "outputs\reports\magic_complete_scan.tsv"
}
foreach($k in $req.Keys){
  $p = $req[$k]
  $ok = Test-Path (J $p)
  $rows.Add((Row "receipt" $k $p ($(if($ok){"PASS"}else{"FAIL"}))))
}

# Restore probe recency (robust parse with regex)
try{
  $restorePath = J "outputs\reports\restore_probe_receipt.txt"
  if(Test-Path $restorePath){
    $line = (Get-Content $restorePath -Tail 1) -join ""
    # Find an ISO timestamp like 2025-09-29T17:08:22
    $m = [regex]::Match($line,'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}')
    if($m.Success){
      $tsStr = $m.Value
      $culture = [System.Globalization.CultureInfo]::InvariantCulture
      $style   = [System.Globalization.DateTimeStyles]::AssumeLocal
      $tsRec = $null
      try { $tsRec = [DateTime]::ParseExact($tsStr,'s',$culture,$style) }
      catch { $tsRec = [DateTime]::Parse($tsStr,$culture) }
      $ageDays = ($tsNow - $tsRec).TotalDays
      $rows.Add((Row "restore" "restore_receipt_age_days" ([math]::Round($ageDays,2)) ($(if($ageDays -le $RecentDays){"PASS"}else{"WARN"})) "≤$RecentDays days"))
    } else {
      $rows.Add((Row "restore" "restore_receipt_parse" $line "WARN" "No ISO timestamp found"))
    }
  } else {
    $rows.Add((Row "restore" "restore_receipt_missing" $restorePath "FAIL"))
  }
} catch {
  $errors.Add($_.Exception.Message)
  $rows.Add((Row "restore" "restore_receipt_parse" "N/A" "WARN" "Could not parse restore receipt timestamp"))
}

# Summaries (array-safe counting)
$pass = @($rows | Where-Object {$_.status -eq "PASS"}).Count
$fail = @($rows | Where-Object {$_.status -eq "FAIL"}).Count
$warn = @($rows | Where-Object {$_.status -eq "WARN"}).Count

# Write outputs
$tsv = J "outputs\reports\status_now.tsv"
$rows | ForEach-Object {
  '{0}`t{1}`t{2}`t{3}`t{4}' -f $_.category,$_.name,$_.value,$_.status,$_.notes
} | Set-Content -Encoding UTF8 $tsv

$json = J "outputs\reports\status_now.json"
@{
  ts     = (Get-Date -Format s)
  counts = @{ total = $rows.Count; pass=$pass; warn=$warn; fail=$fail }
  rows   = $rows
  errors = $errors
} | ConvertTo-Json -Depth 6 | Set-Content -Encoding UTF8 $json

Write-Host "Wrote:`n $tsv`n $json" -ForegroundColor Green
