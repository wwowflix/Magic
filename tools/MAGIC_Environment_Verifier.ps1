param([string]$Root=".", [switch]$SkipDocker, [switch]$Pause)

function Ensure-Dir($p){ if(-not (Test-Path $p)){ New-Item -ItemType Directory -Force -Path $p | Out-Null } }

try { $Root = (Resolve-Path $Root).Path } catch { $Root = Convert-Path $Root }

$ts = Get-Date -Format "yyyyMMdd_HHmmss"
$outDir = Join-Path $Root "outputs\reports\env"; Ensure-Dir $outDir
$checks = @()

# ---- Drive ----
$drv = Split-Path $Root -Qualifier
try {
  $d = Get-PSDrive -Name ($drv.TrimEnd(':'))
  $total = [math]::Round(($d.Used + $d.Free)/1GB,0)
  $free  = [math]::Round($d.Free/1GB,1)
  $checks += [pscustomobject]@{ Check='Drive Letter'; Status='OK'; Detail=("{0}  {1} GB free of {2} GB" -f $drv,$free,$total) }
} catch {
  $checks += [pscustomobject]@{ Check='Drive Letter'; Status='WARN'; Detail=("$drv not found") }
}

# ---- Repo/.git ----
$repoExists = Test-Path $Root
$statusRepo = if ($repoExists) { 'OK' } else { 'ERR' }
$checks += [pscustomobject]@{ Check='Repo Root Exists'; Status=$statusRepo; Detail=$Root }

$gitPresent = Test-Path (Join-Path $Root '.git')
$statusGit = if ($gitPresent) { 'OK' } else { 'WARN' }
$checks += [pscustomobject]@{ Check='.git Present'; Status=$statusGit; Detail='folder' }

# ---- Python / venv ----
$pyv = (& python --version 2>$null)
$statusPy = if ($pyv) { 'OK' } else { 'WARN' }
$checks += [pscustomobject]@{ Check='Python'; Status=$statusPy; Detail=$pyv }

$venvPath = Join-Path $Root 'venv\Scripts\Activate.ps1'
$venv = Test-Path $venvPath
$statusVenv = if ($venv) { 'OK' } else { 'WARN' }
$detailVenv = if ($venv) { 'Found venv\Scripts\Activate.ps1' } else { 'Missing' }
$checks += [pscustomobject]@{ Check='Virtualenv'; Status=$statusVenv; Detail=$detailVenv }

# ---- Tokens (.env) ----
$envFile = Join-Path $Root '.env'
$keys = 'OPENAI_API_KEY','NOTION_TOKEN','CODECOV_TOKEN','REDDIT_CLIENT_ID','REDDIT_SECRET'
foreach ($k in $keys) {
  $has = $false
  if (Test-Path $envFile) {
    $has = Select-String -Path $envFile -Pattern ("^\s*{0}\s*=" -f [regex]::Escape($k)) -Quiet -ErrorAction SilentlyContinue
  }
  $statusKey  = if ($has) { 'OK' } else { 'WARN' }
  $detailKey  = if ($has) { 'Loaded' } else { 'Missing' }
  $checks += [pscustomobject]@{ Check=$k; Status=$statusKey; Detail=$detailKey }
}

# ---- Docker (optional) ----
if (-not $SkipDocker) {
  try {
    $ver = (& docker version --format '{{.Server.Version}}' 2>$null)
    $statusDocker = if ($ver) { 'OK' } else { 'WARN' }
    $detailDocker = if ($ver) { "Server $ver" } else { 'Not reachable' }
    $checks += [pscustomobject]@{ Check='Docker Engine'; Status=$statusDocker; Detail=$detailDocker }
  } catch {
    $checks += [pscustomobject]@{ Check='Docker Engine'; Status='WARN'; Detail='Not reachable' }
  }
}

# ---- Output ----
$tsv = Join-Path $outDir ("env_verify_{0}.tsv" -f $ts)
$json = Join-Path $outDir ("env_verify_{0}.json" -f $ts)
$checks | Select Check,Status,Detail | Export-Csv -Delimiter "`t" -NoTypeInformation -Encoding UTF8 $tsv
$checks | ConvertTo-Json | Set-Content -Encoding UTF8 $json

Write-Host "`n=== Readiness Summary ===`n" -ForegroundColor Cyan
$checks | Format-Table -AutoSize
Write-Host "`nSaved: $tsv`nSaved: $json`n" -ForegroundColor DarkCyan
if ($Pause) { Read-Host "Press Enter to close" }
