param(
  [string]$Root       = 'D:\MAGIC',
  [string]$VenvPy     = 'D:\MAGIC\venv\Scripts\python.exe',
  [string]$Phases     = '0-17',   # change if your runner expects a different format
  [int]   $TimeoutSec = 0         # 0 = no timeout
)

$ErrorActionPreference = 'Stop'

function Parse-Version {
  param([string]$name)
  $ver = [Version]'0.0'
  if($name -match 'self_healing_runner_v(?<v>\d+(?:\.\d+)*)(?:_[^\.]+)?\.py'){
    $parts = @()
    foreach($p in $Matches['v'].Split('.')){ $parts += [int]$p }
    if($parts.Count -eq 1){ $parts += 0 }
    if($parts.Count -gt 4){ $parts = $parts[0..3] }
    switch($parts.Count){
      2 { $ver = New-Object System.Version $parts[0],$parts[1] }
      3 { $ver = New-Object System.Version $parts[0],$parts[1],$parts[2] }
      4 { $ver = New-Object System.Version $parts[0],$parts[1],$parts[2],$parts[3] }
      Default { $ver = [Version]'0.0' }
    }
  }
  return $ver
}

function Get-LatestRunner {
  param([string]$Root = 'D:\MAGIC')

  $cands = Get-ChildItem -Path $Root -Recurse -File -Filter 'self_healing_runner_v*.py' -ErrorAction SilentlyContinue
  if(-not $cands){ return $null }

  $ranked = foreach($f in $cands){
    $name = $f.Name
    $ver  = Parse-Version -name $name
    $isParallel = 0
    if($name -match 'parallel'){ $isParallel = 1 }
    [PSCustomObject]@{
      FullName     = $f.FullName
      VersionObj   = $ver
      ParallelFlag = $isParallel
      Ticks        = $f.LastWriteTime.Ticks
    }
  }

  $best = $ranked |
    Sort-Object -Property @{Expression='VersionObj';Descending=$true},
                           @{Expression='ParallelFlag';Descending=$true},
                           @{Expression='Ticks';Descending=$true} |
    Select-Object -First 1

  if($best){ return $best.FullName } else { return $null }
}

function Get-RunnerModule {
  param([string]$RunnerPath, [string]$Root)
  try{
    $rp  = (Resolve-Path -LiteralPath $RunnerPath).Path
    $rel = $rp.Substring($Root.Length).TrimStart('\','/')
    $mod = ($rel -replace '\.py$','') -replace '[\\/]', '.'
    return $mod
  } catch { return $null }
}

# --- Verify python ---
if(-not (Test-Path $VenvPy)){
  Write-Host "Python venv not found: $VenvPy" -ForegroundColor Red
  exit 1
}

# --- Pick runner ---
$runner = Get-LatestRunner -Root $Root
if(-not $runner){
  Write-Host "No self_healing_runner_v*.py found under $Root" -ForegroundColor Red
  exit 1
}
Write-Host "Using runner: $runner" -ForegroundColor Cyan

# --- Decide if runner supports --phases (avoid fragile --help probing)
$SupportsPhases = ($runner -match 'v5' -or $runner -match 'parallel')

# --- Build args ---
$runnerArgs = @()
if($SupportsPhases -and $Phases){ $runnerArgs += @('--phases', $Phases) }
else { Write-Host "Runner does not support --phases; skipping that arg." -ForegroundColor Yellow }

# --- Execute (module-first so imports like tools.* work) ---
$exitCode = 0
$runnerModule = Get-RunnerModule -RunnerPath $runner -Root $Root

if($TimeoutSec -gt 0){
  $psi = New-Object System.Diagnostics.ProcessStartInfo
  $psi.FileName       = $VenvPy
  if($runnerModule){
    $psi.Arguments    = ("-m {0} {1}" -f $runnerModule, ($runnerArgs -join ' '))
    $psi.WorkingDirectory = $Root
  } else {
    $psi.Arguments    = ('"{0}" {1}' -f $runner, ($runnerArgs -join ' '))
  }
  $psi.UseShellExecute = $false
  $p = [System.Diagnostics.Process]::Start($psi)
  if(-not $p.WaitForExit($TimeoutSec * 1000)){
    try{ $p.Kill() }catch{}
    Write-Host "Runner timed out after $TimeoutSec seconds." -ForegroundColor Red
    exit 124
  }
  $exitCode = $p.ExitCode
} else {
  if($runnerModule){
    Push-Location $Root
    try{
      & $VenvPy -m $runnerModule @runnerArgs
      $exitCode = $LASTEXITCODE
    } finally { Pop-Location }
  } else {
    & $VenvPy $runner @runnerArgs
    $exitCode = $LASTEXITCODE
  }
}

# --- Post-run sync (placeholder) ---
Write-Host "Syncing run results to Notion dashboard (placeholder)."

# --- Write audit of which runner was used ---
$reportDir = Join-Path $Root 'outputs\reports'
New-Item -ItemType Directory -Force -Path $reportDir | Out-Null
"$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')`t$runner" | Out-File (Join-Path $reportDir 'nightly_runner_used.txt') -Append -Encoding UTF8

exit $exitCode
