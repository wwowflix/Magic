param([string]$Root="D:\MAGIC")
$ErrorActionPreference = "Stop"
function J($p){ Join-Path $Root $p }
if(!(Test-Path (J "outputs\reports"))){ New-Item -ItemType Directory -Force -Path (J "outputs\reports") | Out-Null }

$rows = New-Object System.Collections.Generic.List[object]
function Row($cat,$name,$val,$status,$notes=""){ 
  $rows.Add([pscustomobject]@{category=$cat;name=$name;value="$val";status=$status;notes=$notes}) 
}

# Basics
Row "repo" "root_path" $Root "INFO"
Row "repo" "has_git" (Test-Path (J ".git")) ($(if(Test-Path (J ".git")){"PASS"}else{"FAIL"}))

# venv + hooks
Row "python" "venv" (Test-Path (J "venv\Scripts\python.exe")) ($(if(Test-Path (J "venv\Scripts\python.exe")){"PASS"}else{"FAIL"}))
Row "hooks" "pre-commit" (Test-Path (J ".git\hooks\pre-commit")) ($(if(Test-Path (J ".git\hooks\pre-commit")){"PASS"}else{"FAIL"}))

# Receipts (sample subset)
$checks = @{
  "commit"   = "outputs\reports\commit_receipt.txt";
  "push"     = "outputs\reports\push_receipt.txt";
  "tag"      = "outputs\reports\tag_receipt.txt";
  "sbom"     = "outputs\reports\sbom.json";
  "sli"      = "outputs\reports\sli_metrics.json";
  "slo"      = "outputs\reports\slo_enforce.json";
}
foreach($k in $checks.Keys){
  $p = $checks[$k]; $ok = Test-Path (J $p)
  Row "receipt" $k $p ($(if($ok){"PASS"}else{"FAIL"}))
}

# Write outputs
$tsv = (J "outputs\reports\magic_complete_scan.tsv")
$rows | ForEach-Object { '{0}`t{1}`t{2}`t{3}`t{4}' -f $_.category,$_.name,$_.value,$_.status,$_.notes } | 
  Set-Content -Encoding UTF8 $tsv
$json = (J "outputs\reports\magic_complete_scan.json")
$rows | ConvertTo-Json -Depth 5 | Set-Content -Encoding UTF8 $json

Write-Host "Wrote:`n $tsv`n $json" -ForegroundColor Green
