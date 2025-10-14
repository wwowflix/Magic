<# tools\reports\magic_status_export.ps1
   Week 10 – Guard Hardening | Exports PR-ready Markdown status + (optional) guard test proof
#>
[CmdletBinding()]
param([switch]$RunGuardTest)

$ErrorActionPreference = 'Stop'
$Root = (git rev-parse --show-toplevel).Trim()
Set-Location $Root
$outDir = Join-Path $Root 'outputs\reports\readiness'
New-Item -ItemType Directory -Force -Path $outDir | Out-Null
$ts = Get-Date -Format 'yyyyMMdd_HHmmss'
$out = Join-Path $outDir ("MAGIC_STATUS_{0}.md" -f $ts)

function Add([string]$s){ $script:MD += $s + "`r`n`r`n" }

$week   = 'Week 10 – Guard Hardening'
$branch = (git rev-parse --abbrev-ref HEAD) 2>$null
$repo   = $Root

$accept = @"
| Hook surface | Triggered on test? | Blocked files listed | Exit code | .gitignore OK? | Next action |
|---|---|---|---|---|---|
"@

$row = "| Native git shim + local pre-commit | _not-run_ |  |  |  | Keep installed & enabled |"

if($RunGuardTest){
  $gitIgnoreOK = if(git check-ignore -v .env .coverage .artifacts\secret.txt 2>$null){ "Yes" } else { "No" }

  # Stage a forbidden file and attempt a real commit – we expect non-zero rc
  'key=oops' | Set-Content -Encoding UTF8 .env
  git add -f .env | Out-Null

  $stdout = Join-Path $outDir "commit_stdout_$ts.txt"
  $stderr = Join-Path $outDir "commit_stderr_$ts.txt"
  $p = Start-Process git -ArgumentList @('commit','-m','guard proof should fail') -NoNewWindow -Wait -PassThru `
       -RedirectStandardOutput $stdout -RedirectStandardError $stderr
  $rc = $p.ExitCode

  # Clean temp
  git restore --staged .env 2>$null | Out-Null
  Remove-Item .env -Force -EA SilentlyContinue

  $lines = @()
  if(Test-Path $stdout){ $lines += Get-Content $stdout -Raw }
  if(Test-Path $stderr){ $lines += Get-Content $stderr -Raw }
  $blocked = ($lines -split "`r?`n") | Where-Object { $_ -match 'MAGIC_GUARD_BLOCK:' -or $_ -match ' - \.env| - \.coverage| - \.artifacts' }
  $blockedJoined = ($blocked | ForEach-Object { $_.Trim() }) -join '<br>'

  $triggered = if($rc -ne 0){ "Yes" } else { "No (commit went through!)" }
  $row = "| Native git shim + local pre-commit | $triggered | $blockedJoined | $rc | $gitIgnoreOK | Keep installed & enabled |"
}

$script:MD = @()
Add "# MAGIC – Production Readiness Snapshot"
Add "| Field | Value |`n|---|---|`n| Current Week | $week |`n| Repo Path | ``$repo`` |`n| Branch | ``$branch`` |`n| Goal | Block secrets/artifacts; normalize line endings; reliable hooks; prep PR |"
Add "## Acceptance Report (PR-ready)`n$accept`n$row"

$MD | Set-Content -Encoding utf8 $out
Write-Host "✅ Wrote $out" -ForegroundColor Green
