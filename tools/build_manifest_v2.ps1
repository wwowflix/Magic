param(
  [string]$Root = "D:\MAGIC",
  [int]$Phase = 11,
  [switch]$All
)

$ErrorActionPreference = 'Stop'

$Scripts = Join-Path $Root "scripts"
$OutFile = Join-Path $Root "phase_manifest.json"

function Get-ReadyFiles {
  Get-ChildItem -Path $Scripts -Recurse -File -Filter "*_READY.py" -ErrorAction SilentlyContinue
}

# regex helpers to infer Phase/Module
$rePhaseDir  = [regex]'[\\/]+phase(?<num>\d+)[\\/]'
$reModuleDir = [regex]'[\\/]module_(?<mod>[A-Z])[\\/]'
$rePrefix    = [regex]'^(?<num>\d{1,2})(?<mod>[A-Z])[_-]'

function Infer-PhaseModule([System.IO.FileInfo]$File) {
  $p = $File.FullName
  $fn = $File.Name
  $phaseNum = $null
  $mod = $null

  $m1 = $rePhaseDir.Match($p);    if ($m1.Success) { $phaseNum = [int]$m1.Groups['num'].Value }
  $m2 = $reModuleDir.Match($p);   if ($m2.Success) { $mod = $m2.Groups['mod'].Value.ToUpper() }

  if (-not $phaseNum -or -not $mod) {
    $m3 = $rePrefix.Match($fn)
    if ($m3.Success) {
      if (-not $phaseNum) { $phaseNum = [int]$m3.Groups['num'].Value }
      if (-not $mod)      { $mod      = $m3.Groups['mod'].Value.ToUpper() }
    }
  }

  return @{ PhaseNumber = $phaseNum; Module = $mod }
}

function Is-Placeholder([System.IO.FileInfo]$File) {
  try {
    $len = $File.Length
    if ($len -lt 60) { return $true }
    $t = Get-Content $File.FullName -Raw -Encoding UTF8
    if ($t -match '(?i)placeholder') { return $true }
    $t2 = ($t -replace "(\r?\n)+"," " ).Trim()
    $pattern = '^\s*(?:"""|'''''').*?(?:"""|'''''')\s*pass\s*$'
    if ($t2 -match $pattern) { return $true }
    return $false
  } catch { return $true }
}

function Ensure-Noop([int]$P) {
  $tools = Join-Path $Root "tools"
  New-Item -ItemType Directory -Force -Path $tools | Out-Null
  $f = Join-Path $tools ("phase{0}_noop_READY.py" -f $P)
  if (-not (Test-Path $f)) {
    @'
if __name__ == "__main__":
    print("phase noop ok")
'@ | Out-File -FilePath $f -Encoding utf8
  }
  return $f
}

function Build-Manifest {
  param([int]$FocusPhase, [switch]$IncludeAll)

  $entries = @()
  $files = Get-ReadyFiles
  foreach ($f in $files) {
    $inf = Infer-PhaseModule $f
    $pn = $inf.PhaseNumber
    $mod = $inf.Module
    if (-not $pn) { continue }
    if (-not $IncludeAll -and $pn -ne $FocusPhase) { continue }
    if (Is-Placeholder $f) { continue }

    $entries += [PSCustomObject]@{
      PhaseNumber = $pn
      Phase       = $pn
      Module      = $mod
      Path        = $f.FullName
      Command     = 'python "{0}"' -f $f.FullName
    }
  }

  if ($entries.Count -eq 0) {
    $noop = Ensure-Noop $FocusPhase
    $entries += [PSCustomObject]@{
      PhaseNumber = $FocusPhase
      Phase       = $FocusPhase
      Module      = "Z"
      Path        = $noop
      Command     = 'python "{0}"' -f $noop
    }
  }

  $obj = [PSCustomObject]@{ entries = $entries }
  $obj | ConvertTo-Json -Depth 6 | Out-File -FilePath $OutFile -Encoding utf8
  Write-Host ("manifest written: {0} (entries: {1})" -f $OutFile, $entries.Count) -ForegroundColor Green
}

# run the build
Build-Manifest -FocusPhase $Phase -IncludeAll:$All
