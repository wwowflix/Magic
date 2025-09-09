# --- Auto-pick latest self_healing_runner_v*.py ---
function Get-LatestRunner {
  param([string]$Root = 'D:\MAGIC')
  $c = Get-ChildItem -Path $Root -Filter 'self_healing_runner_v*.py' -File -ErrorAction SilentlyContinue
  if(-not $c){ return $null }
  $best = $c | Sort-Object {
    if($_.Name -match 'self_healing_runner_v(?<v>\d+(?:\.\d+)*)\.py'){
      $parts = $Matches['v'].Split('.'); foreach($p in $parts){ [int]$p }
    } else { 0 }
  } -Descending | Select-Object -First 1
  return $best.FullName
}

# Ensure venv python
if(-not (Get-Command 'D:\MAGIC\venv\Scripts\python.exe' -ErrorAction SilentlyContinue)){
  Write-Host "Python venv not found at D:\MAGIC\venv\Scripts\python.exe" -ForegroundColor Red
  exit 1
}
$py = 'D:\MAGIC\venv\Scripts\python.exe'

$runner = Get-LatestRunner -Root 'D:\MAGIC'
if(-not $runner){
  Write-Host "No self_healing_runner_v*.py found under D:\MAGIC" -ForegroundColor Red
  exit 1
}
Write-Host ("Using runner: {0}" -f $runner) -ForegroundColor Cyan
$ErrorActionPreference = "Stop"
Set-Location D:\MAGIC
python self_healing_runner_v5.py --phases 0-17
python tools/notion_sync_agent.py
