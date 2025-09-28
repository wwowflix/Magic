param(
  [string]$Root = "D:\MAGIC",
  [switch]$DryRun
)

$ErrorActionPreference = "Stop"
function J($p){ Join-Path $Root $p }
function Ensure-Dir([string]$p){ if(!(Test-Path $p)){ New-Item -ItemType Directory -Force -Path $p | Out-Null } }

$tsv = J "outputs\reports\magic_complete_scan.tsv"
$cfgPath = J "outputs\config\alerts.json"
$logs = J "outputs\logs"; Ensure-Dir $logs
$reports = J "outputs\reports"; Ensure-Dir $reports

# Load scan
if(!(Test-Path $tsv)){
  Write-Warning "Scan file not found: $tsv"
  @{ ok=$false; reason="scan_missing"; ts=(Get-Date -Format s) } | ConvertTo-Json |
    Set-Content -Encoding UTF8 (J "outputs\reports\ops_notify.json")
  exit 0
}

# Parse TSV → objects
$lines = Get-Content $tsv | Where-Object { $_ -and $_.Contains("`t") }
$objects = foreach($ln in $lines){
  $parts = $ln -split "`t",5
  if($parts.Count -ge 4){
    [pscustomobject]@{
      category = $parts[0]
      name     = $parts[1]
      value    = $parts[2]
      status   = $parts[3]
      notes    = $(if($parts.Count -ge 5){$parts[4]} else {""})
    }
  }
}

$fails = $objects | Where-Object { $_.status -match 'FAIL' }
$warns = $objects | Where-Object { $_.status -match 'WARN' }
$passes= $objects | Where-Object { $_.status -match 'PASS' }

$summary = @{
  ts     = (Get-Date -Format s)
  counts = @{
    total = $objects.Count
    pass  = $passes.Count
    warn  = $warns.Count
    fail  = $fails.Count
  }
  top_fails = $fails | Select-Object -First 10 category,name,value,notes
}

# Build Slack text
$text = @()
$text += "*MAGIC Nightly Scan* (`$(Get-Date -Format s)`)"
$text += ("• PASS: {0}  WARN: {1}  FAIL: {2}" -f $passes.Count, $warns.Count, $fails.Count)
if($fails.Count -gt 0){
  $text += ""
  $text += "*Top FAIL items:*"
  foreach($f in $summary.top_fails){
    $text += ("• `{0}` – {1} ({2}) {3}" -f $f.category, $f.name, $f.value, $f.notes)
  }
} else {
  $text += "✅ No failures detected."
}

# Read alerts config (may be empty)
$webhook = ""
if(Test-Path $cfgPath){
  try { $cfg = Get-Content $cfgPath | ConvertFrom-Json; $webhook = "$($cfg.slack_webhook)" } catch {}
}

# Decide delivery
$receipt = J "outputs\reports\ops_notify.json"
if([string]::IsNullOrWhiteSpace($webhook)){
  # no webhook: write receipt & log
  $summary | ConvertTo-Json -Depth 5 | Set-Content -Encoding UTF8 $receipt
  Set-Content -Encoding UTF8 (J "outputs\logs\notify_preview.txt") ($text -join "`r`n")
  Write-Host "No webhook configured. Wrote receipt + preview log." -ForegroundColor Yellow
} else {
  # send to Slack unless DryRun
  $payload = @{ text = ($text -join "`n") } | ConvertTo-Json -Compress
  if($DryRun){
    $summary.delivery = "dry_run"
    $summary | ConvertTo-Json -Depth 5 | Set-Content -Encoding UTF8 $receipt
    Set-Content -Encoding UTF8 (J "outputs\logs\notify_preview.txt") ($text -join "`r`n")
    Write-Host "DryRun: would have posted to Slack." -ForegroundColor Yellow
  } else {
    try{
      Invoke-RestMethod -Uri $webhook -Method Post -ContentType 'application/json' -Body $payload
      $summary.delivery = "slack_sent"
      $summary | ConvertTo-Json -Depth 5 | Set-Content -Encoding UTF8 $receipt
      Write-Host "Slack notification sent." -ForegroundColor Green
    } catch {
      $summary.delivery = "slack_error"
      $summary.error = $_.Exception.Message
      $summary | ConvertTo-Json -Depth 5 | Set-Content -Encoding UTF8 $receipt
      Write-Host "Slack send failed, wrote receipt." -ForegroundColor Red
    }
  }
}


