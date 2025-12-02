# ================================
# MAGIC Nightly Orchestrator wrapper
# Stage 5 – Step 5.5 (Nightly Scheduled Runs)
# ================================
$ErrorActionPreference = "Stop"

$root = "E:\MAGIC"
Set-Location -LiteralPath $root

# 1) Activate venv if present
$venv = Join-Path $root "venv\Scripts\Activate.ps1"
if (Test-Path $venv) {
    . $venv
} else {
    Write-Host "[WARN] venv missing at $venv – continuing without activation."
}

# 2) Ensure logs folder exists
$logRoot = Join-Path $root "outputs\logs\nightly"
if (-not (Test-Path $logRoot)) {
    New-Item -ItemType Directory -Path $logRoot -Force | Out-Null
}

$stamp   = Get-Date -Format "yyyyMMdd_HHmmss"
$logPath = Join-Path $logRoot "magic_nightly_$stamp.log"

function Write-Log {
    param([string]$msg)
    $line = "[{0}] {1}" -f (Get-Date), $msg
    $line | Tee-Object -FilePath $logPath -Append
}

Write-Log "Starting MAGIC nightly orchestrator."

# 3) Locate orchestrator
$orchestrator = Join-Path $root "tools\Magic_Orchestrator_Master_v3.ps1"
if (-not (Test-Path $orchestrator)) {
    Write-Log "ERROR: Orchestrator not found at $orchestrator"
    exit 1
}

# 4) Run orchestrator and capture exit code
try {
    & $orchestrator *>> $logPath
    $exit = $LASTEXITCODE
} catch {
    Write-Log ("EXCEPTION: " + $_.Exception.Message)
    $exit = 1
}

Write-Log ("Finished orchestrator with exit code = {0}" -f $exit)

# 5) Retain only last 7 logs (simple rotation)
try {
    Get-ChildItem -Path $logRoot -Filter "magic_nightly_*.log" |
        Sort-Object LastWriteTime -Descending |
        Select-Object -Skip 7 |
        Remove-Item -Force -ErrorAction SilentlyContinue
} catch {
    Write-Log ("Log rotation warning: " + $_.Exception.Message)
}

exit $exit
