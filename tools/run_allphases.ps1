# --- Auto-pick latest self_healing_runner_v*.py ---
function Get-LatestRunner {
  param([string]$Root = 'D:\MAGIC')

  $cands = Get-ChildItem -Path $Root -Recurse -File -Filter 'self_healing_runner_v*.py' -ErrorAction SilentlyContinue
  if(-not $cands){ return $null }

  $ranked = foreach($f in $cands){
    $name = $f.Name
    $full = $f.FullName
    $ver  = 0
    # match v5, v4.9, v5_parallel, v5.1_rc, etc.
    if($name -match 'self_healing_runner_v(?<v>\d+(?:\.\d+)*)(?:_[^\.]+)?\.py'){
      $nums = $Matches['v'].Split('.') | ForEach-Object {[int]# --- Auto-pick latest self_healing_runner_v*.py ---
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
$runner =  Get-LatestRunner -Root 'D:\MAGIC'
if(-not $runner){
  Write-Host "No self_healing_runner_v*.py found under D:\MAGIC" -ForegroundColor Red
  exit 1
}
Write-Host ("Using runner: {0}" -f $runner) -ForegroundColor Cyan
$ErrorActionPreference = "Stop"
Set-Location D:\MAGIC
& $py $runner --phases 0-17
python tools/notion_sync_agent.py
}
      # convert array of ints into a big numeric rank (e.g., [5,1] -> 5*1e6 + 1)
      $rank = 0
      foreach($n in $nums){ $rank = ($rank * 1000) + $n }
      $ver = $rank
    }
    $isParallel = ($name -match 'parallel') ? 1 : 0
    [PSCustomObject]@{
      FullName     = $full
      VersionRank  = $ver
      ParallelFlag = $isParallel
      Ticks        = $f.LastWriteTime.Ticks
    }
  }

  $best = $ranked |
    Sort-Object -Property @{Expression='VersionRank';Descending=$true},
                           @{Expression='ParallelFlag';Descending=$true},
                           @{Expression='Ticks';Descending=$true} |
    Select-Object -First 1

  if($best){ return $best.FullName } else { return $null }
}

# Ensure venv python
if(-not (Get-Command 'D:\MAGIC\venv\Scripts\python.exe' -ErrorAction SilentlyContinue)){
  Write-Host "Python venv not found at D:\MAGIC\venv\Scripts\python.exe" -ForegroundColor Red
  exit 1
}
$py = 'D:\MAGIC\venv\Scripts\python.exe'
$runner =  Get-LatestRunner -Root 'D:\MAGIC'
if(-not $runner){
  Write-Host "No self_healing_runner_v*.py found under D:\MAGIC" -ForegroundColor Red
  exit 1
}
Write-Host ("Using runner: {0}" -f $runner) -ForegroundColor Cyan
$ErrorActionPreference = "Stop"
Set-Location D:\MAGIC
& $py $runner --phases 0-17
python tools/notion_sync_agent.py
