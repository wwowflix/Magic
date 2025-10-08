param(
  [string]$TablePath = ".\outputs\reports\readiness\status_live_latest.tsv",
  [switch]$AutogenIfMissing,
  [switch]$SkipDocker,
  [switch]$Pause
)
function Ensure-Dir($p){ if(-not (Test-Path $p)){ New-Item -ItemType Directory -Force -Path $p | Out-Null } }
$root = Get-Location
$abs  = if([IO.Path]::IsPathRooted($TablePath)){ $TablePath } else { Join-Path $root $TablePath }
Ensure-Dir (Split-Path $abs -Parent)

# Autogenerate a 56-row baseline if missing
if(-not (Test-Path $abs) -and $AutogenIfMissing){
  $rows = @()
  $weekPlan = @{
    0=1; 1=5; 2=4; 3=4; '3.5'=1; 4=3; 5=5; '5.5'=1; 6=9; 7=9; 8=2; 9=2; 10=3; 11=2; 12=5; 99=1
  }
  $seed = @(
    'Env verifier','Folder scan','Status test','Create .env','Create venv',
    'Install requirements','Git remote setup','Docker build -t magic:1.0 .','Add Docker HEALTHCHECK',
    'Canary publish (sandbox)'
  )
  foreach($k in $weekPlan.Keys){
    $w = [string]$k
    $n = [int]$weekPlan[$k]
    for($i=0;$i -lt $n;$i++){
      $act = if($i -lt $seed.Count){ $seed[$i] } else { "Task $($i+1)" }
      $rows += [pscustomobject]@{
        Week = $w
        Area = 'Release'
        'Action (PowerShell / Command)' = $act
        Status = '⏭ Not Started'
      }
    }
  }
  $rows | Export-Csv -Delimiter "`t" -NoTypeInformation -Encoding UTF8 $abs
  Write-Host "Created baseline status table → $abs" -ForegroundColor Green
}

if(Test-Path $abs){
  $rows = Import-Csv -Delimiter "`t" $abs
  $done = ($rows | Where-Object { $_.Status -match '✅|(?i)done' }).Count
  $ip   = ($rows | Where-Object { $_.Status -match '⏳|(?i)progress' }).Count
  $ns   = $rows.Count - $done - $ip
  $pct  = if($rows.Count){ [math]::Round(($done/$rows.Count)*100,1) } else { 0 }

  Write-Host "`n=== MAGIC STATUS SUMMARY ===" -ForegroundColor Cyan
  Write-Host ("Overall: {0}%  (✅{1}/⏳{2}/⏭{3} of {4})" -f $pct,$done,$ip,$ns,$rows.Count) -ForegroundColor Green

  $sumDir = Join-Path (Split-Path $abs -Parent) ''
  $ts = Get-Date -Format "yyyyMMdd_HHmmss"
  ($rows | ConvertTo-Json -Depth 4) | Set-Content -Encoding UTF8 (Join-Path $sumDir ("status_summary_{0}.json" -f $ts))
  "Percent`t$Pct`nDone`t$done`nInProgress`t$ip`nNotStarted`t$ns`nTotal`t$($rows.Count)" |
    Set-Content -Encoding UTF8 (Join-Path $sumDir ("status_summary_{0}.tsv" -f $ts))
}else{
  Write-Warning "Table not found: $abs (use -AutogenIfMissing to create)"
}
if($Pause){ Read-Host "Press Enter to close" }
