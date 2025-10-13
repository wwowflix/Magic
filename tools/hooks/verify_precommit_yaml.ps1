param([string]$Path = ".pre-commit-config.yaml")

if(-not (Test-Path $Path)){
  Write-Error "YAML error: '$Path' not found. Create it before running the verifier."
  exit 3
}

# Fail if BOM present
$bytes = [IO.File]::ReadAllBytes($Path)
if($bytes.Length -gt 2 -and $bytes[0]-eq0xEF -and $bytes[1]-eq0xBB -and $bytes[2]-eq0xBF){
  Write-Error "YAML error: UTF-8 BOM detected in $Path — rewrite without BOM."
  exit 4
}

$raw = Get-Content $Path -Raw
# Any flush-left "- repo" is invalid; must be under "repos:"
if($raw -match "(?m)^\- repo"){
  Write-Error "YAML error: top-level '- repo' at column 1; indent under 'repos:'."
  exit 2
}
Write-Host "✔ $Path looks structurally OK (no BOM, no flush-left '- repo')."
