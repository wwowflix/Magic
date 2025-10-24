[CmdletBinding()]
param(
  [string]$Root = ".",
  [int]$SprintTargetPct = 75,
  [int]$CurrentOverallPct = 70
)

$ErrorActionPreference = "Stop"
Set-Location $Root

function Try-ReadJson($path){
  if(Test-Path $path){ try { return Get-Content $path -Raw -Encoding UTF8 | ConvertFrom-Json } catch { } }
  return $null
}
function Try-ReadTsv($path){
  if(Test-Path $path){
    $rows = @()
    Get-Content $path -Encoding UTF8 | Select-Object -Skip 1 | ForEach-Object {
      if($_.Trim()){ $rows += ,($_ -split "`t") }
    }
    return $rows
  }
  return @()
}
function Latest-Coverage(){
  $hist = "outputs/reports/coverage/coverage_history.tsv"
  if(Test-Path $hist){
    $lines = Get-Content $hist -Encoding UTF8 | Where-Object {$_ -and -not $_.StartsWith("#")}
    if($lines.Count -gt 1){
      $cols = $lines[-1] -split "`t"
      if($cols.Count -ge 2){ return ($cols[1] -replace '%','') }
    }
  }
  return $null
}

# read signals
$proofPath  = "outputs/reports/ci/proof_bundle_receipt.json"
$proof      = Try-ReadJson $proofPath
$proofOk    = [bool]$proof
$proofSizes = if($proof){ ($proof.sizes | ConvertTo-Json -Compress) } else { "{}" }

$bootPct = Latest-Coverage
if(-not $bootPct){ $bootPct = "0" }

$microPath     = "outputs/reports/tests/microtest_matrix.tsv"
$micro         = Try-ReadTsv $microPath
$microAdded    = ($micro | Where-Object { $_.Count -ge 3 -and $_[2] -match '^(1|true|yes)$' }).Count
$microPassing  = ($micro | Where-Object { $_.Count -ge 4 -and $_[3] -match '^(1|true|yes)$' }).Count

# Heuristic bump for Week 11
[int]$overall = $CurrentOverallPct
if([double]$bootPct -ge 5){ $overall += 3 }
if($proofOk){ $overall += 2 }
if($microAdded -ge 10 -and [double]$bootPct -ge 10){ $overall += 3 }
if($overall -gt 100){ $overall = 100 }

# console dashboard
Write-Host ""
Write-Host "MAGIC Completion Dashboard — LOCAL (Week 11)" -ForegroundColor Cyan
Write-Host "Now (est): $overall%     Target: $SprintTargetPct%" -ForegroundColor Yellow
Write-Host ""

$proofText = $( if($proofOk) { "bundle:+ sizes=$proofSizes" } else { "bundle:–" } )

$rows = @()
$rows += [pscustomobject]@{ Area="CI & Coverage Bootstrap"; Now="$bootPct% boot";             Goal="≥10%"; Proof=$proofText }
$rows += [pscustomobject]@{ Area="Minimal Test Baseline";  Now="$microPassing passing / $microAdded added"; Goal="10–15"; Proof="tests/microtest_matrix.tsv" }
$rows += [pscustomobject]@{ Area="Week 11 B status";       Now=("proof:{0}; cov={1}%" -f ($(if($proofOk){"ok"}else{"pending"}), $bootPct)); Goal="≥10%"; Proof=$proofPath }

$rows | Format-Table -AutoSize | Out-String -Width 200 | Write-Host

# outputs
$outDir = "outputs/reports/status"
New-Item -ItemType Directory -Force $outDir | Out-Null
$tsv  = Join-Path $outDir "status_now.tsv"
$json = Join-Path $outDir "status_now.json"

"key`tvalue" | Out-File -Encoding UTF8 $tsv
@(
  "week`t11",
  "overall_pct`t$overall",
  "target_pct`t$SprintTargetPct",
  "coverage_boot_pct`t$bootPct",
  "proof_bundle`t" + ($(if($proofOk){"present"}else{"absent"})),
  "microtests_added`t$microAdded",
  "microtests_passing`t$microPassing",
  "proof_sizes_json`t$proofSizes"
) | Add-Content -Encoding UTF8 $tsv

$payload = [pscustomobject]@{
  week = 11
  overall_pct = $overall
  target_pct  = $SprintTargetPct
  coverage_boot_pct = [double]$bootPct
  proof_bundle = $proofOk
  proof_sizes  = $proof.sizes
  microtests = @{ added = $microAdded; passing = $microPassing }
  generated_at = (Get-Date).ToString("s")
}
$payload | ConvertTo-Json -Depth 5 | Out-File -Encoding UTF8 $json

Write-Host ""
Write-Host "Wrote:" -ForegroundColor Green
Write-Host "  $tsv"
Write-Host "  $json"
