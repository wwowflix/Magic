# Week 10 pending checker (Pester 3.4 compatible) — ROBUST PATHS

$ErrorActionPreference = 'Stop'
$PSDefaultParameterValues['*:Encoding'] = 'utf8'

function Get-RepoRoot {
  if ($env:MAGIC_ROOT -and (Test-Path $env:MAGIC_ROOT)) { return $env:MAGIC_ROOT }
  if ($PSScriptRoot) {
    $root = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
    if (Test-Path $root) { return $root }
  }
  try {
    $gitRoot = (git rev-parse --show-toplevel) 2>$null
    if ($gitRoot -and (Test-Path $gitRoot.Trim())) { return $gitRoot.Trim() }
  } catch {}
  if (Test-Path 'D:\MAGIC') { return 'D:\MAGIC' }
  return (Get-Location).Path
}

$ROOT = Get-RepoRoot

function Resolve-MetricsPath {
  if ($env:METRICS_PATH -and (Test-Path $env:METRICS_PATH)) { return $env:METRICS_PATH }
  $primary = Join-Path $ROOT 'outputs\metrics\cleanup_metrics.json'
  if (Test-Path $primary) { return $primary }
  # fallback: search under outputs\metrics for the newest cleanup_metrics.json
  $cand = Get-ChildItem -Path (Join-Path $ROOT 'outputs\metrics') -Filter 'cleanup_metrics.json' -Recurse -ErrorAction SilentlyContinue |
          Sort-Object LastWriteTime -Desc | Select-Object -First 1
  if ($cand) { return $cand.FullName }
  return $primary  # return the expected path (may not exist)
}

$metricsPath   = Resolve-MetricsPath
$retryReqDir   = Join-Path $ROOT 'outputs\retry_requests'
$failOnPending = $env:FAIL_ON_PENDING -eq '1'

Write-Host "Resolved ROOT: $ROOT"
Write-Host "Resolved metricsPath: $metricsPath"

function Get-LatestCleanupMetrics {
  if (-not (Test-Path $metricsPath)) { return $null }
  try {
    $raw = Get-Content $metricsPath -Raw
    $arr = ConvertFrom-Json $raw
    # If file is a single object, wrap it to behave like an array
    if ($arr -isnot [System.Collections.IEnumerable] -or $arr.PSObject.TypeNames -contains 'System.Management.Automation.PSCustomObject') {
      # ConvertFrom-Json returns PSCustomObject for a single object
      if ($arr -and $arr.PSObject.Properties.Count -gt 0 -and -not ($arr -is [System.Array])) {
        $arr = @($arr)
      }
    }
    if ($arr -is [System.Collections.IEnumerable]) {
      # handle ArrayList or Object[]
      $count = 0; try { $count = $arr.Count } catch { $count = @($arr).Count }
      if ($count -gt 0) { return $arr[$count-1] }
    }
  } catch {}
  return $null
}

function Get-RecentRetryRequest {
  if (-not (Test-Path $retryReqDir)) { return $null }
  $file = Get-ChildItem $retryReqDir -Filter 'cleanup_retry_*.json' -ErrorAction SilentlyContinue |
          Sort-Object LastWriteTime -Desc | Select-Object -First 1
  if (-not $file) { return $null }
  try {
    $obj = Get-Content $file.FullName -Raw | ConvertFrom-Json
    return [pscustomobject]@{ Path=$file.FullName; Obj=$obj; LastWrite=$file.LastWriteTime }
  } catch { return $null }
}

$now    = Get-Date
$cutoff = $now.AddHours(-48)

# 10.3 — Cleanup agent ran recently AND did actual work
$latest      = Get-LatestCleanupMetrics
$step10_3_ok = $false
$note10_3    = "metrics not found"
if ($latest) {
  $ts      = $latest.ts
  $parsed  = $null
  try { $parsed = [datetime]::Parse(($ts -replace 'Z$')) } catch {}
  $activity = [int](0 + $latest.removed_files) + [int](0 + $latest.compressed) + [int](0 + $latest.removed_dirs)
  if ($parsed -and $parsed -gt $cutoff -and $activity -gt 0) {
    $step10_3_ok = $true
    $note10_3 = "last=$($parsed.ToString('u')), activity=$activity"
  } else {
    $note10_3 = "last=$ts, activity=$activity (need run in last 48h with work)"
  }
}

# 10.4 — Chaos test produced retry request with basenames recently
$recentRetry  = Get-RecentRetryRequest
$step10_4_ok  = $false
$note10_4     = "no retry_requests/cleanup_retry_*.json"
if ($recentRetry) {
  $count = 0
  try { $count = @($recentRetry.Obj.basenames).Count } catch { $count = 0 }
  if ($count -gt 0 -and $recentRetry.LastWrite -gt $cutoff) {
    $step10_4_ok = $true
    $note10_4 = "retry file: $($recentRetry.Path) ($count basenames)"
  } else {
    $note10_4 = "retry file stale or empty: $($recentRetry.Path)"
  }
}

# 10.5 — Prefer tag to mark Done. Branch alone => pending.
$step10_5_ok = $false
$note10_5    = "tag v0.10.4 not found"
try {
  $hasTag    = (git tag --list v0.10.4) -ne ''
  $hasBranch = (git branch --list 'feat/failover-10x','week10-failover' | Select-String .) -ne $null
  if ($hasTag) {
    $step10_5_ok = $true
    $note10_5 = "tag v0.10.4 present"
  } elseif ($hasBranch) {
    $note10_5 = "branch present; tag pending"
  }
} catch { $note10_5 = "git unavailable" }

$rows = @()
$rows += [pscustomobject]@{ Step='10.3'; Name='Cleanup agent + metrics';       Status=$(if ($step10_3_ok) {'Done'} else {'Pending'}); Notes=$note10_3 }
$rows += [pscustomobject]@{ Step='10.4'; Name='Chaos test (seed→clean→retry)'; Status=$(if ($step10_4_ok) {'Done'} else {'Pending'}); Notes=$note10_4 }
$rows += [pscustomobject]@{ Step='10.5'; Name='Commit/tag failover branch';    Status=$(if ($step10_5_ok) {'Done'} else {'Pending'}); Notes=$note10_5 }

$rows | Format-Table -AutoSize

Describe 'Week 10 Pending Gate (Pester 3.4)' {
  Context '10.3' {
    if ($step10_3_ok) {
      It 'should be Done' { $true | Should Be $true }
    } elseif ($failOnPending) {
      It 'should be Done (forced fail on pending)' { $true | Should Be $false }
    } else {
      Write-Warning "Pending: $note10_3"
      It 'is Pending' -Pending { }
    }
  }
  Context '10.4' {
    if ($step10_4_ok) {
      It 'should be Done' { $true | Should Be $true }
    } elseif ($failOnPending) {
      It 'should be Done (forced fail on pending)' { $true | Should Be $false }
    } else {
      Write-Warning "Pending: $note10_4"
      It 'is Pending' -Pending { }
    }
  }
  Context '10.5' {
    if ($step10_5_ok) {
      It 'should be Done' { $true | Should Be $true }
    } elseif ($failOnPending) {
      It 'should be Done (forced fail on pending)' { $true | Should Be $false }
    } else {
      Write-Warning "Pending: $note10_5"
      It 'is Pending' -Pending { }
    }
  }
}

$pending = $rows | Where-Object { $_.Status -ne 'Done' }
if ($pending.Count -gt 0) {
  Write-Host "`nPending steps:" -ForegroundColor Yellow
  $pending | Format-Table -AutoSize
}
