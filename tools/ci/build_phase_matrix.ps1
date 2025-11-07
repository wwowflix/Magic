param(
  [int]$Phase = 11,
  [string]$Root = (Get-Location).Path,
  [switch]$Pretty
)

$ErrorActionPreference = 'Stop'

# Local fallback for GitHub Actions env var
if (-not $env:GITHUB_OUTPUT -or [string]::IsNullOrWhiteSpace($env:GITHUB_OUTPUT)) {
  $env:GITHUB_OUTPUT = Join-Path -Path $Root -ChildPath '_gh_output.txt'
}

$phaseDir = Join-Path $Root ("scripts\phase{0}" -f $Phase)
if (-not (Test-Path -LiteralPath $phaseDir)) { throw "Phase directory not found: $phaseDir" }

$mods = Get-ChildItem -LiteralPath $phaseDir -Directory -Filter 'module_*' -EA SilentlyContinue |
  ForEach-Object { ($_.Name -replace '^module_','').ToUpper() } |
  Where-Object { $_ -match '^[A-Z]{1,2}$' } |
  Sort-Object -Unique

if (-not $mods) { throw "No modules discovered under $phaseDir" }

# Build matrix
$obj = @{ include = @() }
foreach ($m in $mods) { $obj.include += @{ module = $m } }

if ($Pretty) {
  $json = $obj | ConvertTo-Json -Depth 5
  $eof = "EOF$([guid]::NewGuid().ToString('N'))"
  Add-Content -Encoding UTF8 -Path $env:GITHUB_OUTPUT -Value "matrix<<$eof"
  Add-Content -Encoding UTF8 -Path $env:GITHUB_OUTPUT -Value $json
  Add-Content -Encoding UTF8 -Path $env:GITHUB_OUTPUT -Value $eof
} else {
  $json = $obj | ConvertTo-Json -Depth 5 -Compress
  Add-Content -Encoding UTF8 -Path $env:GITHUB_OUTPUT -Value ("matrix=$json")
}

Write-Host ("Discovered modules: {0}" -f ($mods -join ', '))
Write-Host ("Matrix JSON ({0}): {1}" -f ($(if($Pretty){"pretty"}else{"compressed"}), $json))
Write-Host ("Output file: {0}" -f $env:GITHUB_OUTPUT)
