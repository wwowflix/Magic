[CmdletBinding()]
param(
  [string]$Root = (Get-Location).Path,
  [int]$SamplePerModule = 2,
  [switch]$Strict,
  [switch]$RunOrchestratorIfMissing,
  [string]$PythonExe = "",
  [string]$SmokePattern = "",
  [int]$MaxPreview = 400
)

$ErrorActionPreference = 'Stop'

function Out-Status { param([string]$Label,[string]$State,[string]$Note='')
  $c = switch($State){ 'PASS'{'Green'} 'WARN'{'Yellow'} default{'Red'} }
  "{0,-32} {1,-6} {2}" -f $Label, $State, $Note | Write-Host -ForegroundColor $c
}

function Resolve-Python { param([string]$Given)
  if ($Given -and (Test-Path $Given)) { return (Resolve-Path $Given).Path }
  $venvPy = Join-Path $Root "venv\Scripts\python.exe"
  if (Test-Path $venvPy) { return (Resolve-Path $venvPy).Path }
  return "python"
}

$python = Resolve-Python -Given:$PythonExe
Out-Status "Hello" "PASS" "msc_min OK"
