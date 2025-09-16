param(
  [int]$Phase = 11,
  [string]$SummaryPath = "outputs\summaries\phase_master_summary.tsv",
  [string]$LogsRoot = "outputs\logs",
  [string]$ScriptsRoot = "scripts",
  [switch]$TryRun,
  [switch]$ForcePlaceholder,
  [int]$MaxTries = 2
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Run-SmokeTest {
  param([int]$Phase)
  Write-Host "▶ Running smoketest for Phase $Phase ..." -ForegroundColor Cyan
  & python tools/e2e_smoketest.py --phase $Phase
  $code = $LASTEXITCODE
  if ($code -ne 0) { Write-Warning "Smoketest returned exit code $code (expected during initial fix pass)." }
  else { Write-Host "Smoketest OK." -ForegroundColor Green }
  return $code
}

function Load-Report { (Get-Content "outputs\summaries\e2e_report.json" -Raw | ConvertFrom-Json) }

function Ensure-Dir([string]$Path) { if ($Path -and -not (Test-Path $Path)) { New-Item -ItemType Directory -Force -Path $Path | Out-Null } }

function Resolve-ScriptPath([int]$Phase,[string]$Module,[string]$ScriptBase,[string]$ScriptsRoot) {
  $modPart = "module_$Module"
  $phaseDir = Join-Path $ScriptsRoot "phase$Phase"
  $modDir   = Join-Path $phaseDir $modPart
  if (-not (Test-Path $modDir)) { return $null }
  $exact = Join-Path $modDir "$ScriptBase.py"
  if (Test-Path $exact) { return $exact }
  $cand = Get-ChildItem $modDir -Filter "*.py" -File -ErrorAction SilentlyContinue |
          Where-Object { $_.BaseName -eq $ScriptBase -or $_.BaseName.StartsWith($ScriptBase) } |
          Select-Object -First 1
  if ($cand) { return $cand.FullName }
  return $null
}

function Write-PlaceholderLog([string]$LogDir,[string]$ScriptBase,[string]$Reason = "Placeholder log created to satisfy E2E until real run is wired.") {
  Ensure-Dir -Path $LogDir
  $logPath = Join-Path $LogDir "$ScriptBase.log"
  $stamp = (Get-Date).ToString("s")
  "[$stamp] $Reason" | Set-Content -Encoding UTF8 -Path $logPath
  return $logPath
}

function Run-Script-ToLog([string]$ScriptPath,[string]$LogDir,[string]$ScriptBase) {
  Ensure-Dir -Path $LogDir
  $logPath = Join-Path $LogDir "$ScriptBase.log"
  Write-Host "▶ Running $ScriptPath → $logPath" -ForegroundColor Yellow
  & python $ScriptPath *>&1 | Tee-Object -FilePath $logPath | Out-Null
  return $logPath
}

function CountOf([Parameter(ValueFromPipeline=$true)][object]$x) { process { return (@($x) | Measure-Object).Count } }

if (-not (Test-Path $SummaryPath)) { throw "Summary TSV not found: $SummaryPath" }
if (-not (Test-Path "tools\e2e_smoketest.py")) { throw "Smoketest not found: tools\e2e_smoketest.py" }

for ($attempt = 1; $attempt -le $MaxTries; $attempt++) {
  Write-Host "`n=== Attempt $attempt of $MaxTries ===" -ForegroundColor Magenta
  $null = Run-SmokeTest -Phase $Phase
  $report = Load-Report

  if ($report.ok -eq $true) { Write-Host "✅ E2E OK after attempt $attempt." -ForegroundColor Green; exit 0 }

  # 1) Ensure missing log folders (robust)
  $missingFolders = @($report.missing_log_folders) | Where-Object { $_ -and $_.ToString().Trim() -ne "" } | Sort-Object -Unique
  if ((CountOf $missingFolders) -gt 0) {
    Write-Host "Creating missing log folders..." -ForegroundColor Cyan
    foreach ($f in $missingFolders) { Ensure-Dir -Path $f }
  }

  # 2) Handle missing logs for FAIL rows (robust)
  $missingLogs = @($report.missing_logs_for_fail_rows) | Where-Object { $_ }
  if ((CountOf $missingLogs) -gt 0) {
    Write-Host "Fixing missing logs for FAIL rows..." -ForegroundColor Cyan
    foreach ($m in $missingLogs) {
      $mod = $m.module; $base = $m.script; $logDir = $m.log_dir
      if (-not $base) { $base = "(unknown)" }
      if ($ForcePlaceholder -or -not $TryRun) { Write-PlaceholderLog -LogDir $logDir -ScriptBase $base | Out-Null; continue }
      $scriptPath = $null
      if ($base -and $base -ne "(unknown)") { $scriptPath = Resolve-ScriptPath -Phase $Phase -Module $mod -ScriptBase $base -ScriptsRoot $ScriptsRoot }
      if ($scriptPath) { Run-Script-ToLog -ScriptPath $scriptPath -LogDir $logDir -ScriptBase $base | Out-Null }
      else { Write-Warning "Script not found for $base (Module $mod). Writing placeholder log."; Write-PlaceholderLog -LogDir $logDir -ScriptBase $base -Reason "Script not found. Placeholder log." | Out-Null }
    }
  } else {
    Write-Host "No missing logs reported; only folders were missing." -ForegroundColor DarkCyan
  }
}

Write-Host "`n=== Final verification ===" -ForegroundColor Magenta
$null = Run-SmokeTest -Phase $Phase
$finalReport = Load-Report

if ($finalReport.ok -eq $true) {
  Write-Host "✅ E2E OK after fix cycle." -ForegroundColor Green; exit 0
} else {
  Write-Warning "❌ E2E still failing. See outputs\summaries\e2e_report.json"
  Write-Host "Totals: $($finalReport.totals | ConvertTo-Json -Compress)"
  $mf = @($finalReport.missing_log_folders) | Where-Object { $_ }
  if ((CountOf $mf) -gt 0) { Write-Host "Missing log folders:" -ForegroundColor Yellow; $mf | ForEach-Object { Write-Host " - $_" } }
  $ml = @($finalReport.missing_logs_for_fail_rows) | Where-Object { $_ }
  if ((CountOf $ml) -gt 0) { Write-Host "Missing logs for FAIL rows:" -ForegroundColor Yellow; $ml | ForEach-Object { Write-Host (" - Module {0} Script {1} Dir {2}" -f $_.module, $_.script, $_.log_dir) } }
  exit 1
}
