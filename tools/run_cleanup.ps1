param(
  [int]$OlderThanDays = 14,
  [string]$Mode = "aggressive"  # try "delete" for hard removal
)

# 1) Locate a cleanup agent dynamically
$agent = Get-ChildItem -Recurse -File -Include `
  "*cleanup*agent*.py","*cleanup*runner*.py","*cleanup*.py" `
  -Path .\tools,.\scripts,.\agents,.\utilities,.\modules 2>$null |
  Sort-Object FullName |
  Select-Object -First 1 -ExpandProperty FullName

if (-not $agent) {
  Write-Error "Cleanup agent not found under tools/, scripts/, agents/, utilities/, or modules/.";
  exit 1
}

# 2) Ensure metrics destination exists
$report = "outputs\metrics\cleanup_metrics.json"
New-Item -ItemType Directory -Path (Split-Path $report) -Force | Out-Null

# 3) Build common args
$common = @(
  "--include","outputs/logs/**",
  "--include","outputs/temp/**",
  "--include","outputs/cache/**",
  "--older-than-days",$OlderThanDays,
  "--report",$report
)

# 4) Prefer --mode, fallback to --action
$cmd = @("python", $agent) + $common + @("--mode",$Mode)
& $cmd[0] $cmd[1..($cmd.Length-1)]
if ($LASTEXITCODE -ne 0) {
  Write-Host "Retrying with --action instead of --mode..."
  $cmd = @("python", $agent) + $common + @("--action",$Mode)
  & $cmd[0] $cmd[1..($cmd.Length-1)]
}

# 5) Show the last two metric entries
if (Test-Path $report) {
  "`nLatest cleanup metrics entries:"
  (Get-Content $report -Raw | ConvertFrom-Json | Select-Object -Last 2) | Format-List
} else {
  Write-Warning "No metrics file written at $report"
}
