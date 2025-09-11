# tools\magic_todo_audit.ps1
# Audits remaining tasks (Weeks 4–12) by checking for receipts.

param(
  [string]$Root = "D:\MAGIC"
)

$ErrorActionPreference = 'Stop'
Set-Location $Root
$Reports = Join-Path $Root "outputs\reports"
New-Item -ItemType Directory -Force -Path $Reports | Out-Null

function Test-ContainsLine {
  param([string]$Path,[string]$Pattern)
  if (-not (Test-Path $Path)) { return $false }
  $c = Get-Content $Path -Raw
  return [bool]([regex]::IsMatch($c,$Pattern,"IgnoreCase"))
}

$items = @(
  @{Week=4; Step="4.3 Alerts"; What="Slack/email alert in CI"; Evidence=@(@{Type="line";Path=".github\workflows\self_heal.yml";Pattern="slack|smtp"})},
  @{Week=8; Step="8.3 Documentation"; What="Runbook & Remediation guide"; Evidence=@(@{Type="file";Path="docs\runbook.md"},@{Type="file";Path="docs\remediation_guide.md"})},
  @{Week=8; Step="8.4 Team demo"; What="Recorded walkthrough"; Evidence=@(@{Type="fileAny";Paths=@("docs\demos\week8_demo.mp4","docs\demos\week8_demo.md")})},
  @{Week=9; Step="9.1 Stress test"; What="1000-script simulation"; Evidence=@(@{Type="file";Path="outputs\reports\stress_test_1000.tsv"})}
  # … keep adding all the items like before …
)

$result = foreach ($it in $items) {
  $allPass=$true; $gaps=@()
  foreach ($ev in $it.Evidence) {
    $ok=$false
    switch ($ev.Type) {
      "file" { $ok=Test-Path (Join-Path $Root $ev.Path) }
      "fileAny" { foreach($p in $ev.Paths){ if(Test-Path (Join-Path $Root $p)){ $ok=$true;break}}}
      "line" { $ok=Test-ContainsLine (Join-Path $Root $ev.Path) $ev.Pattern }
    }
    if(-not $ok){$allPass=$false; $gaps+=$ev.Path}
  }
  [PSCustomObject]@{Week=$it.Week;Step=$it.Step;What=$it.What;Status=if($allPass){"Done"}else{"Missing"};Gaps=($gaps -join "; ")}
}

$flat = $result | Sort-Object Week,Step
$flat | Format-Table -AutoSize

$tsv=Join-Path $Reports "magic_todo_audit.tsv"
$md =Join-Path $Reports "magic_todo_audit.md"
$flat | Export-Csv -Delimiter "`t" -NoTypeInformation -Path $tsv -Encoding utf8

$lines=@("# MAGIC – To-Do Audit","","| Week | Step | What | Status | Gaps |","|-----:|------|------|--------|------|")
foreach($row in $flat){
  $lines+="| {0} | {1} | {2} | {3} | {4} |" -f $row.Week,$row.Step,$row.What,$row.Status,($row.Gaps -replace '\r?\n',' ')
}
$lines -join "`r`n" | Out-File -FilePath $md -Encoding utf8

Write-Host "`nSaved:" -ForegroundColor Green
Write-Host " - $tsv"
Write-Host " - $md"
