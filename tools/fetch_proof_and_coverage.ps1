param(
  [string]$RunId = $(gh run list --limit 1 --json databaseId | ConvertFrom-Json | Select-Object -First 1 -ExpandProperty databaseId)
)
$ErrorActionPreference='Stop'
if(-not $RunId){ Write-Warning "No recent run found"; exit 1 }

function Try-Download($name, $dir){
  try { gh run download $RunId --name $name --dir $dir; return $true } catch { return $false }
}

$dl = "outputs/reports/ci/download/$RunId"
New-Item -ItemType Directory -Force $dl | Out-Null
Write-Host "Downloading artifacts from run $RunId ..." -ForegroundColor Cyan

$got = Try-Download "proof-bundle" $dl
if(-not $got){
  Write-Warning "proof-bundle missing; trying proof-bundle-aux"
  $got = Try-Download "proof-bundle-aux" $dl
}

if(-not $got){
  Write-Warning "No valid artifacts found to download"
  exit 0
}

$cov = Join-Path $dl "coverage.xml"
if(!(Test-Path $cov)){
  Write-Warning "coverage.xml missing in artifact (ok if you downloaded -aux)"
  exit 0
}

[string]$raw = Get-Content $cov -Raw
[xml]$x = $raw
$rate = $null
try {
  if($x.coverage -and $x.coverage.Attributes["line-rate"]){
    $rate = [double]$x.coverage.Attributes["line-rate"].Value * 100
  } elseif ($x.coverage -and $x.coverage.Attributes["lines-covered"] -and $x.coverage.Attributes["lines-valid"]) {
    $covered = [double]$x.coverage.Attributes["lines-covered"].Value
    $valid   = [double]$x.coverage.Attributes["lines-valid"].Value
    if($valid -gt 0){ $rate = ($covered * 100.0 / $valid) }
  }
} catch { }
if($null -eq $rate -and $raw -match 'line-rate="([0-9.]+)"'){ $rate = [double]$matches[1] * 100 }
if($null -eq $rate){ $rate = 0 }

$bpct = ("{0:N2}" -f $rate); $fpct = $bpct

$hist = "outputs/reports/coverage/coverage_history.tsv"
New-Item -ItemType Directory -Force (Split-Path $hist) | Out-Null
if(!(Test-Path $hist)){ "date`tboot_pct`tfull_pct" | Out-File -Encoding utf8 $hist }
"$((Get-Date).ToString('s'))`t$bpct`t$fpct" | Add-Content -Encoding utf8 $hist

Write-Host "Bootstrap Coverage: $bpct%" -ForegroundColor Green
