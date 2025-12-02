Param([switch]$NoZip)

$ErrorActionPreference = "Stop"
Set-Location (Resolve-Path ".")

# Ensure output dirs
New-Item -ItemType Directory -Force -Path .\outputs\reports, .\outputs\proofs | Out-Null

# State
$now     = Get-Date -Format "yyyyMMdd_HHmmss"
$outTsv  = ".\outputs\reports\where_am_i_now_$now.tsv"
$outJson = ".\outputs\reports\where_am_i_now_$now.json"
$zipOut  = ".\outputs\proofs\where_am_i_now_$now.zip"

# Collector
$script:rows = @()

function Add-Row {
    param($Stage, $Check, $Pass, $Evidence, $Notes)
    $script:rows += [pscustomobject]@{
        Stage    = $Stage
        Check    = $Check
        Status   = if ($Pass) { "PASS" } else { "FAIL" }
        Evidence = $Evidence
        Notes    = $Notes
    }
}

# ---- Git baseline
$branch = (git rev-parse --abbrev-ref HEAD) 2>$null
$dirty  = (git status --porcelain) 2>$null
$tags   = (git tag --list) 2>$null

Add-Row 'ALL'    'Git branch'               ($branch -ne $null)     $branch   ''
Add-Row 'ALL'    'Working tree clean'       ($dirty -eq '')          ('lines=' + (($dirty | Measure-Object -Line).Lines)) 'Fail ⇒ unstaged/uncommitted changes'
Add-Row 'STAGE 3' 'Tag v1.0-stable present' ($tags -match 'v1\.0-stable') (($tags | Select-String 'v1\.0-stable') -join ',') ''

# ---- Stage 1
$ready = Get-ChildItem -Recurse -File -Filter "*_READY.py" .\scripts -ErrorAction SilentlyContinue
$tiny = @()
foreach($f in $ready){
  try{
    if((Get-Content -LiteralPath $f.FullName -Raw -ErrorAction Stop).Length -lt 20){ $tiny += $f.FullName }
  }catch{}
}
Add-Row 'STAGE 1' 'READY.py count'           ($ready.Count -gt 0)    ("count=$($ready.Count)") 'Expect ~900 when complete'
Add-Row 'STAGE 1' 'No tiny/empty READY.py'   ($tiny.Count  -eq 0)    ("tiny=$($tiny.Count)")   'Fail ⇒ generation not completed'

# ---- Stage 2
$lock = Test-Path .\requirements.lock.txt
$sbom = Test-Path .\outputs\reports\sbom.json
Add-Row 'STAGE 2' 'requirements.lock.txt exists' $lock '.\requirements.lock.txt' ''
Add-Row 'STAGE 2' 'SBOM exists'                  $sbom '.\outputs\reports\sbom.json' ''
if ($sbom){
  try { $null = Get-Content .\outputs\reports\sbom.json -Raw | ConvertFrom-Json; Add-Row 'STAGE 2' 'SBOM valid JSON' $true  'parse ok' '' }
  catch { Add-Row 'STAGE 2' 'SBOM valid JSON' $false 'parse error' $_.Exception.Message }
}

# ---- Stage 3
Add-Row 'STAGE 3' 'CODEOWNERS present'       (Test-Path .\.github\CODEOWNERS)                '.github/CODEOWNERS' ''
Add-Row 'STAGE 3' 'PR template present'      (Test-Path .\.github\pull_request_template.md)  '.github/pull_request_template.md' ''

# ---- Stage 4
try {
  $dockerOk = (docker version) 2>$null
  Add-Row 'STAGE 4' 'Docker CLI available'   ($dockerOk -ne $null) '' ''
  $img = (docker images --format "{{.Repository}}:{{.Tag}}" | Select-String "^magic:1\.0$") 2>$null
  Add-Row 'STAGE 4' 'Image magic:1.0 exists' ($img -ne $null) ($img -join ',') ''
  if ($img){
    try {
      $null = (docker run --rm magic:1.0 python tools/healthcheck.py) 2>$null
      Add-Row 'STAGE 4' 'Container healthcheck script runs' ($LASTEXITCODE -eq 0) ('exitcode=' + $LASTEXITCODE) ''
    } catch { Add-Row 'STAGE 4' 'Container healthcheck script runs' $false '' $_.Exception.Message }
  }
} catch { Add-Row 'STAGE 4' 'Docker CLI available' $false '' $_.Exception.Message }

# ---- Stage 5
Add-Row 'STAGE 5' 'features.json exists'     (Test-Path .\config\features.json)         '.\config\features.json' ''
Add-Row 'STAGE 5' 'alerts slack.json exists' (Test-Path .\config\alerts\slack.json)     '.\config\alerts\slack.json' ''
Add-Row 'STAGE 5' 'SLI metrics present'      (Test-Path .\outputs\metrics\sli.json)     '.\outputs\metrics\sli.json' ''
Add-Row 'STAGE 5' 'SLO report present'       (Test-Path .\outputs\reports\slo_report.tsv) '.\outputs\reports\slo_report.tsv' ''

# ---- Stage 6
Add-Row 'STAGE 6' 'cleanup_plan.tsv present'        (Test-Path .\outputs\reports\cleanup_plan.tsv)        '.\outputs\reports\cleanup_plan.tsv' ''
Add-Row 'STAGE 6' 'magic_full_status.json present'  (Test-Path .\outputs\reports\magic_full_status.json)   '.\outputs\reports\magic_full_status.json' ''
$releaseZip = Get-ChildItem .\backups -Filter "release_v1.0.zip" -ErrorAction SilentlyContinue
Add-Row 'STAGE 6' 'release_v1.0.zip exists' ($releaseZip -ne $null) ($releaseZip.FullName) ''

# ---- Stage 7
Add-Row 'STAGE 7' 'stage7_status.json present'      (Test-Path .\outputs\status\stage7_status.json)        '.\outputs\status\stage7_status.json' ''
Add-Row 'STAGE 7' 'release_verification.json present' (Test-Path .\outputs\status\release_verification.json) '.\outputs\status\release_verification.json' ''

# ---- Stage 8
Add-Row 'STAGE 8' 'AI outputs folder exists'        (Test-Path .\outputs\ai)                      '.\outputs\ai' ''
Add-Row 'STAGE 8' 'ai_trend_report.tsv present'     (Test-Path .\outputs\ai\ai_trend_report.tsv)  '.\outputs\ai\ai_trend_report.tsv' ''
Add-Row 'STAGE 8' 'v2_manifest.json present'        (Test-Path .\outputs\status\v2_manifest.json) '.\outputs\status\v2_manifest.json' ''

# ---- Write TSV & JSON
$script:rows | ConvertTo-Csv -Delimiter "`t" -NoTypeInformation | Out-File -FilePath $outTsv -Encoding UTF8

$summary = [ordered]@{
  generated_at    = (Get-Date).ToString("s")
  branch          = $branch
  tag_v1_0_stable = [bool]($tags -match 'v1\.0-stable')
  totals          = @{
    pass = ($script:rows | Where-Object {$_.Status -eq 'PASS'}).Count
    fail = ($script:rows | Where-Object {$_.Status -eq 'FAIL'}).Count
  }
  details         = $script:rows
}
$summary | ConvertTo-Json -Depth 6 | Out-File -FilePath $outJson -Encoding UTF8

# ---- Zip (optional)
if (-not $NoZip) {
  $proofList = @(
    $outTsv, $outJson,
    '.\.github\CODEOWNERS', '.\.github\pull_request_template.md',
    '.\requirements.lock.txt', '.\outputs\reports\sbom.json',
    '.\outputs\reports\magic_full_status.json',
    '.\outputs\reports\slo_report.tsv',
    '.\outputs\metrics\sli.json'
  ) | Where-Object { Test-Path $_ }
  if (Test-Path $zipOut) { Remove-Item $zipOut -Force }
  Compress-Archive -Path $proofList -DestinationPath $zipOut -Force
}

Write-Host "== DONE ==" -ForegroundColor Green
Write-Host "TSV : $outTsv"
Write-Host "JSON: $outJson"
if (-not $NoZip) { Write-Host "ZIP : $zipOut" }
