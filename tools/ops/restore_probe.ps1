param(
  [string]$Root = $Root,
  [string]$RclonePath = $null
)


if (-not \E:\MAGIC) { \E:\MAGIC = (Get-Location).Path }
# Basic helpers
function Ensure-Dir([string]$p){
  if(-not (Test-Path $p)){ New-Item -ItemType Directory -Force -Path $p | Out-Null }
}

$logDir = Join-Path $Root "outputs\logs"
Ensure-Dir $logDir
$log = Join-Path $logDir "rclone_restore_task.log"
$receipt = Join-Path $Root "outputs\reports\restore_probe_receipt.txt"

try{
  # Resolve rclone path if not supplied
  if([string]::IsNullOrWhiteSpace($RclonePath)){
    try { $RclonePath = (Get-Command rclone).Source } catch {}
  }
  if(-not $RclonePath -or -not (Test-Path $RclonePath)){
    # last-resort fallbacks
    $candidates = @(
      "$Env:USERPROFILE\scoop\shims\rclone.exe",
      "C:\Program Files\rclone\rclone.exe",
      "C:\Program Files (x86)\rclone\rclone.exe",
      "E:\MAGIC\rclone-v1.70.3-windows-amd64\rclone.exe",
      "rclone.exe"
    )
    foreach($c in $candidates){
      if(Test-Path $c){ $RclonePath = $c; break }
    }
  }

  if(-not (Test-Path $RclonePath)){
    throw "Could not resolve path to rclone.exe"
  }

  # Restore destination
  $restoreDir = Join-Path $Root "outputs\restore_probe"
  Ensure-Dir $restoreDir

  # Compose args (plain array)
  $args = @(
    "copy",
    "remote:MAGIC/outputs/reports",
    $restoreDir,
    "--update",
    "--use-server-modtime",
    "--log-file", $log,
    "--log-level", "INFO"
  )

  # Log the exe used
  Add-Content -Path $log -Value ("[{0}] Using rclone: {1}" -f (Get-Date -Format s), $RclonePath)
  Add-Content -Path $log -Value ("[{0}] Args: {1}" -f (Get-Date -Format s), ($args -join ' '))

  # Invoke rclone directly; capture output and exit code
  $output = & "$RclonePath" @args 2>&1 | Out-String
  $exitCode = $LASTEXITCODE

  Add-Content -Path $log -Value ("[{0}] Output:`n{1}" -f (Get-Date -Format s), $output)
  Add-Content -Path $log -Value ("[{0}] ExitCode: {1}" -f (Get-Date -Format s), $exitCode)

  if($exitCode -ne 0){
    throw "rclone exited with code $exitCode"
  }

  # Write receipt on success
  "restore drill ok $(Get-Date -Format s)" | Set-Content -Encoding UTF8 $receipt
  Write-Host "Restore probe complete. Receipt written to $receipt" -ForegroundColor Green
  exit 0

} catch {
  $msg = "[{0}] ERROR: {1}" -f (Get-Date -Format s), $_.Exception.Message
  Add-Content -Path $log -Value $msg
  "restore drill FAILED $(Get-Date -Format s): $($msg)" | Set-Content -Encoding UTF8 $receipt
  Write-Host $msg -ForegroundColor Red
  exit 1
}
