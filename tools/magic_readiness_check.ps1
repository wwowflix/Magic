[CmdletBinding()]
param(
  [string]$Root = (Get-Location).Path,
  [switch]$EmitMarkdown,
  [switch]$EmitJson,
  [switch]$RunPytests,
  [switch]$OpenReport
)

$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$here   = (Resolve-Path $Root).Path
$tools  = Join-Path $here 'tools'
$outDir = Join-Path $here 'outputs\reports'
$logDir = Join-Path $here 'outputs\logs'
$null = New-Item -ItemType Directory -Force -Path $outDir,$logDir | Out-Null

function Run-Step {
  param([string]$Name,[scriptblock]$Block)
  $sw = [System.Diagnostics.Stopwatch]::StartNew()
  try {
    $r = & $Block
    [pscustomobject]@{ Name=$Name; Status='PASS'; Detail=$r; ms=$sw.ElapsedMilliseconds }
  } catch {
    [pscustomobject]@{ Name=$Name; Status='FAIL'; Detail=$_.Exception.Message; ms=$sw.ElapsedMilliseconds }
  }
}

function Soft-Run {
  param([string]$Name,[scriptblock]$Block)
  $sw = [System.Diagnostics.Stopwatch]::StartNew()
  try {
    $r = & $Block
    [pscustomobject]@{ Name=$Name; Status='INFO'; Detail=$r; ms=$sw.ElapsedMilliseconds }
  } catch {
    [pscustomobject]@{ Name=$Name; Status='WARN'; Detail=$_.Exception.Message; ms=$sw.ElapsedMilliseconds }
  }
}

function Invoke-Tool {
  param([string]$Path, [string[]]$Args)
  if (-not (Test-Path $Path)) { return [pscustomobject]@{ ok=$false; code=1; out="$Path missing" } }

  $outFile = "$logDir\$(Split-Path -Leaf $Path).stdout.txt"
  $errFile = "$logDir\$(Split-Path -Leaf $Path).stderr.txt"

  # Build a -Command that runs the script and merges all streams to stdout
  $argsEscaped = @()
  foreach ($a in ($Args + @('-Root', $Root))) {
    $argsEscaped += ("'{0}'" -f ($a -replace "'", "''"))
  }
  $cmd = ("& {{ & '{0}' {1} *>&1 }}" -f $Path, ($argsEscaped -join ' '))

  $psi = @{
    FilePath               = 'powershell'
    ArgumentList           = @('-NoProfile','-ExecutionPolicy','Bypass','-Command', $cmd)
    RedirectStandardOutput = $outFile
    RedirectStandardError  = $errFile
    PassThru               = $true
    Wait                   = $true
    NoNewWindow            = $true
  }
  $p = Start-Process @psi
  $out = Get-Content $outFile -Raw -ErrorAction SilentlyContinue
  [pscustomobject]@{ ok=($p.ExitCode -eq 0); code=$p.ExitCode; out=$out }
}

function Parse-SelfTest {
  param([string]$text)
  $lines = $text -split "`r?`n"
  $list = New-Object System.Collections.Generic.List[object]

  foreach ($line in $lines) {
    if ($line -match '^\s*(?<emoji>✅|⚠️|❌)\s*(?<title>.+)') {
      $st = switch ($matches.emoji) { '✅' {'PASS'} '⚠️' {'WARN'} '❌' {'FAIL'} default {'INFO'} }
      $list.Add([pscustomobject]@{ Step=$matches.title.Trim(); Status=$st }); continue
    }
    if ($line -match '^\s*\[?(?<status>PASS|WARN|FAIL)\]?\s*[:\-–]\s*(?<title>.+)') {
      $list.Add([pscustomobject]@{ Step=$matches.title.Trim(); Status=$matches.status }); continue
    }
    if ($line -match '^\s*(?<title>.+?)\s+\bOK\b\s*$') {
      $list.Add([pscustomobject]@{ Step=$matches.title.Trim(); Status='PASS' }); continue
    }
    if ($line -match '^\s*(?<num>\d+)\.\s*(?<title>.+?)\s*[-:]\s*(?<status>PASS|WARN|FAIL)') {
      $list.Add([pscustomobject]@{ Step=("Step " + $matches.num + ": " + $matches.title.Trim()); Status=$matches.status })
    }
  }

  if ($list.Count -eq 0) {
    $sum = 'UNKNOWN'
    if ($text -match 'ALL\s*Complete|✅\s*Complete') { $sum = 'PASS' }
    elseif ($text -match 'WARN|⚠️') { $sum = 'WARN' }
    elseif ($text -match 'FAIL|❌') { $sum = 'FAIL' }
    $list.Add([pscustomobject]@{ Step='Self-test summary'; Status=$sum })
  }

  return $list.ToArray()
}

function Repo-Signals {
  $signals = [ordered]@{}
  $signals['Root']     = $here
  $signals['OnBranch'] = (git rev-parse --abbrev-ref HEAD).Trim()

  $null = & git symbolic-ref -q --short HEAD 2>$null
  $signals['Detached'] = ($LASTEXITCODE -ne 0)

  $gitDir = (git rev-parse --git-dir).Trim()
  $signals['RebaseInProgress'] = (Test-Path (Join-Path $gitDir 'rebase-merge')) -or (Test-Path (Join-Path $gitDir 'rebase-apply'))
  $signals['LatestSHA']       = (git rev-parse --short HEAD).Trim()
  $signals['Tag_v1.0-stable'] = [bool](git tag --list 'v1.0-stable')
  $signals['PR_ci-setup']     = $null
  $signals['GitHubCLI']       = (& { gh --version >$null 2>&1; if ($LASTEXITCODE -eq 0) {'yes'} else {'no'} })
  if ($signals['GitHubCLI'] -eq 'yes') {
    $signals['PR_ci-setup'] = (gh pr list --state all --head ci-setup --json url -q '.[0].url' 2>$null)
  }
  $signals['CoverageXML']     = Test-Path (Join-Path $here 'coverage.xml')
  $signals['HTMLCov']         = Test-Path (Join-Path $here 'htmlcov\index.html')
  $signals['ActionsWorkflow'] = Test-Path (Join-Path $here '.github\workflows\tests.yml')

  # Add Coverage%
  if ($signals['CoverageXML']) {
    try {
      [xml]$cov = Get-Content (Join-Path $here 'coverage.xml')
      $rate = [double]$cov.coverage.'line-rate'
      $signals['Coverage%'] = ("{0:N1}" -f ($rate*100))
    } catch {
      $signals['Coverage%'] = 'parse-error'
    }
  }

  [pscustomobject]$signals
}

# ---------- 1) Fresh snapshot (soft) ----------
$scan = Soft-Run 'Snapshot: magic_full_scan.ps1' {
  (Invoke-Tool (Join-Path $tools 'magic_full_scan.ps1') @()).out
}

# ---------- 2) Gatekeeper (hard) ----------
$gate = Run-Step 'Gate: magic_self_test.ps1' {
  $res = Invoke-Tool (Join-Path $tools 'magic_self_test.ps1') @()
  if (-not $res.ok) { throw "magic_self_test.ps1 exit code $($res.code)" }
  $res.out
}

$gateText  = if ($null -ne $gate.Detail) { [string]$gate.Detail } else { '' }
$gateItems = @( Parse-SelfTest -text $gateText )

[int]$pass  = @($gateItems | Where-Object { $_.Status -eq 'PASS' }).Count
[int]$warn  = @($gateItems | Where-Object { $_.Status -eq 'WARN' }).Count
[int]$fail  = @($gateItems | Where-Object { $_.Status -eq 'FAIL' }).Count
[int]$total = @($gateItems).Count
$completion = if ($total -gt 0) { [math]::Round((($pass + 0.5*$warn)/$total)*100,2) } else { 0 }

# ---------- 3) Status digest (soft) ----------
$stat = Soft-Run 'Digest: magic_scan_status.ps1' {
  (Invoke-Tool (Join-Path $tools 'magic_scan_status.ps1') @()).out
}

# ---------- 4) Repo/GitHub signals ----------
$signals = Repo-Signals

# ---------- 5) Optional heavy unit test re-run ----------
$pytest = $null
if ($RunPytests) {
  $pytest = Soft-Run 'PyTests' {
    $p = Start-Process -FilePath 'pytest' -ArgumentList @('-q','--maxfail=1','--cov','--cov-report=term','--cov-report=xml') -NoNewWindow -PassThru -Wait
    if ($p.ExitCode -ne 0) { throw "pytest exit code $($p.ExitCode)" }
    if (Test-Path .\coverage.xml) { Get-Content .\coverage.xml -Raw } else { 'no coverage.xml (term-only report)' }
  }
}

# ---------- 6) Assemble reports ----------
$report = [ordered]@{
  generated_utc = (Get-Date).ToUniversalTime().ToString("s") + "Z"
  root          = "$here"
  completion    = $completion
  counts        = @{ pass=$pass; warn=$warn; fail=$fail; total=$total }
  gate_summary  = ($gateItems | Sort-Object Step)
  signals       = $signals
  snapshot_note = $scan.Status
  digest_note   = $stat.Status
}

# JSON
if ($EmitJson) {
  $jsonPath = Join-Path $outDir 'readiness_status.json'
  ($report | ConvertTo-Json -Depth 6) | Set-Content -Encoding utf8 -Path $jsonPath
  Write-Host ("JSON: {0}" -f $jsonPath)
}

# Markdown
if ($EmitMarkdown) {
  $mdPath = Join-Path $outDir 'readiness_status.md'
  $md = New-Object System.Collections.Generic.List[string]

  $md.Add('# MAGIC Production Readiness - Status')
  $md.Add('')
  $md.Add( ('- **Root:** `{0}`' -f $report.root) )
  $md.Add( ('- **Generated:** {0}' -f $report.generated_utc) )
  $md.Add( ('- **Completion:** **{0}%**  (PASS={1}, WARN={2}, FAIL={3}, Total={4})' -f $report.completion, $pass, $warn, $fail, $total) )
  $md.Add('')
  $md.Add('## Signals')
  $md.Add('')
  $md.Add('| Signal | Value |')
  $md.Add('|---|---|')
  foreach ($p in $signals.PSObject.Properties) {
    $md.Add( ('| {0} | {1} |' -f $p.Name, $p.Value) )
  }
  $md.Add('')
  $md.Add('## Gate - Detailed Checks')
  $md.Add('')
  $md.Add('| Check | Status |')
  $md.Add('|---|---|')
  foreach ($gi in $gateItems) {
    $em = switch ($gi.Status) { 'PASS' {'✅'} 'WARN' {'⚠️'} 'FAIL' {'❌'} default {'·'} }
    $md.Add( ('| {0} | {1} {2} |' -f $gi.Step, $em, $gi.Status) )
  }
  $md.Add('')
  $md.Add('## Notes')
  $md.Add( ('- Snapshot (magic_full_scan.ps1): {0}' -f $scan.Status) )
  $md.Add( ('- Digest (magic_scan_status.ps1): {0}' -f $stat.Status) )
  if ($pytest) { $md.Add( ('- PyTests: {0}' -f $pytest.Status) ) }

  $md -join "`r`n" | Set-Content -Encoding utf8 -Path $mdPath
  Write-Host ("MD:  {0}" -f $mdPath)
  if ($OpenReport) { Start-Process $mdPath | Out-Null }
}

# ---------- 7) Console summary ----------
$line = "Completion: $completion% (PASS=$pass, WARN=$warn, FAIL=$fail, Total=$total)"
$line | Write-Host
if ($fail -gt 0) { exit 2 } elseif ($warn -gt 0) { exit 1 } else { exit 0 }
