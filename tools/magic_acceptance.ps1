# ==== MAGIC ACCEPTANCE CHECK ====
$Root   = "D:\MAGIC"
$Venv   = Join-Path $Root "venv"
$PyExe  = Join-Path $Venv "Scripts\python.exe"
$EnvFile= Join-Path $Root ".env"
$Sorter = Join-Path $Root "scripts\phase0\0A_sorter_READY.py"

function Show([string]$name, [bool]$pass, [string]$note="") {
  $sym = if ($pass) { "✅" } else { "❌" }
  $fg  = if ($pass) { "Green" } else { "Red" }
  $pad = ($name + " ").PadRight(30)
  if ($note) { Write-Host "$pad $sym $note" -ForegroundColor $fg }
  else       { Write-Host "$pad $sym"       -ForegroundColor $fg }
}
function ShowWarn([string]$name, [string]$note) {
  $pad = ($name + " ").PadRight(30)
  Write-Host "$pad ⚠️ $note" -ForegroundColor Yellow
}

Write-Host "==== MAGIC ACCEPTANCE CHECK ====" -ForegroundColor Cyan

# 1) .env
$envPresent = Test-Path $EnvFile
Show ".env present" $envPresent

# 2) venv + python
$venvExists = Test-Path $Venv
Show "venv folder exists" $venvExists

$pyExists = Test-Path $PyExe
if ($pyExists) {
  Show "venv Python found" $true $PyExe
  try {
    $ver = & $PyExe -c "import sys; print(sys.version.split()[0])"
    Show "Python version" $true $ver
  } catch {
    Show "Python version" $false $_.Exception.Message
  }
} else {
  Show "venv Python found" $false
  ShowWarn "Python version" "skip (no venv python)"
}

# 3) requirements.txt
$reqFile = Join-Path $Root "requirements.txt"
Show "requirements.txt present" (Test-Path $reqFile)

# 4) Git (optional)
$gitDir = Join-Path $Root ".git"
if (Test-Path $gitDir) {
  try {
    $gitVersion = (git -C $Root --version) 2>$null
    Show "Git available" $true $gitVersion
    $status = (git -C $Root status --porcelain)
    $clean = [string]::IsNullOrWhiteSpace($status)
    $note  = if ($clean) { "clean" } else { "pending changes" }
    Show "Git clean working tree" $clean $note
  } catch {
    Show "Git available" $false $_.Exception.Message
  }
} else {
  ShowWarn "Git check" "No .git detected"
}

# 5) Phase 0 sorter
Show "0A_sorter_READY.py present" (Test-Path $Sorter)
if ((Test-Path $Sorter) -and $pyExists) {
  try {
    $null = & $PyExe $Sorter --help 2>$null
    Show "Sorter runnable" $true "help shown"
  } catch {
    Show "Sorter runnable" $false $_.Exception.Message
  }
} else {
  ShowWarn "Sorter runnable" "skip"
}

Write-Host "`n==== ACCEPTANCE COMPLETE ====" -ForegroundColor Cyan
