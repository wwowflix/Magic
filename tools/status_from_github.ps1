[CmdletBinding()]
param(
  [string]$Repo = "wwowflix/Magic",
  [int]$Week = 11
)
$ErrorActionPreference = "Stop"

function Get-AuthHeader {
  if($env:GITHUB_TOKEN){ return @{ Authorization = "Bearer $($env:GITHUB_TOKEN)" } }
  try{
    $t = (gh auth token) 2>$null
    if($LASTEXITCODE -eq 0 -and $t){ return @{ Authorization = "Bearer $t" } }
  } catch {}
  return @{}
}
$h = Get-AuthHeader
$ua = @{ "User-Agent" = "MAGIC-status" }
$base = "https://api.github.com/repos/$Repo"

function GET($u){
  try{ Invoke-RestMethod -Method GET -Uri $u -Headers ($h + $ua) }catch{ Write-Warning "GET failed: $u"; $null }
}

$repo = GET "$base"
$arts = GET "$base/actions/artifacts?per_page=100"
$runs = GET "$base/actions/runs?per_page=10"

$proof = $false; $proofAux = $false
$proofSizes = @{}
if($arts -and $arts.artifacts){
  foreach($a in $arts.artifacts){
    if($a.name -eq "proof-bundle"){ $proof = $true; $proofSizes[$a.name] = $a.size_in_bytes }
    if($a.name -eq "proof-bundle-aux"){ $proofAux = $true; $proofSizes[$a.name] = $a.size_in_bytes }
  }
}
$latestRun = $null
if($runs -and $runs.workflow_runs){
  $latestRun = $runs.workflow_runs | Sort-Object created_at | Select-Object -Last 1
}

[int]$overall = 70
if($proof){ $overall += 2 }
if($proofAux){ $overall += 1 }

$outDir = "outputs/reports/status"
New-Item -ItemType Directory -Force $outDir | Out-Null
$tsv  = Join-Path $outDir "status_remote.tsv"
$json = Join-Path $outDir "status_remote.json"

"key`tvalue" | Out-File -Encoding UTF8 $tsv
@(
  "week`t$Week",
  "repo`t$Repo",
  "visibility`t$($repo.visibility)",
  "default_branch`t$($repo.default_branch)",
  "open_issues`t$($repo.open_issues_count)",
  "language`t$($repo.language)",
  "last_push_utc`t$($repo.pushed_at)",
  "proof_bundle`t" + ($(if($proof){"present"}else{"absent"})),
  "proof_bundle_aux`t" + ($(if($proofAux){"present"}else{"absent"})),
  "proof_sizes_json`t" + ($(ConvertTo-Json $proofSizes -Compress)),
  "latest_run_id`t$($latestRun.id)",
  "latest_run_status`t$($latestRun.status)",
  "latest_run_conclusion`t$($latestRun.conclusion)",
  "overall_estimate_pct`t$overall"
) | Add-Content -Encoding UTF8 $tsv

$payload = [pscustomobject]@{
  week = $Week
  repo = $Repo
  visibility = $repo.visibility
  default_branch = $repo.default_branch
  open_issues = $repo.open_issues_count
  language = $repo.language
  last_push_utc = $repo.pushed_at
  artifacts = ($arts.artifacts | Where-Object { $_.name -like "proof-bundle*" } | Select-Object name, size_in_bytes, expired, created_at)
  latest_run = $latestRun
  overall_estimate_pct = $overall
  generated_at = (Get-Date).ToString("s")
}
$payload | ConvertTo-Json -Depth 6 | Out-File -Encoding UTF8 $json

Write-Host "MAGIC Remote Status — $Repo (Week $Week)" -ForegroundColor Cyan
Write-Host ("Proof bundle: {0}, Aux: {1}" -f ($(if($proof){"yes"}else{"no"}), $(if($proofAux){"yes"}else{"no"})))
Write-Host "Wrote:`n  $tsv`n  $json"
