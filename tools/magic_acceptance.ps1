param()

$ErrorActionPreference = "SilentlyContinue"

Write-Host "==== MAGIC ACCEPTANCE CHECK ===="

# Resolve repo root based on script location
$root = (Resolve-Path "$PSScriptRoot\..").Path

# 1) .env present
$envPath = Join-Path $root ".env"
if (Test-Path $envPath) {
    "{0,-26} found" -f ".env present" | Write-Host
} else {
    "{0,-26} missing" -f ".env present" | Write-Host
}

# 2) venv folder exists
$venv = Join-Path $root "venv"
if (Test-Path $venv) {
    "{0,-26} found" -f "venv folder exists" | Write-Host
} else {
    "{0,-26} missing" -f "venv folder exists" | Write-Host
}

# 3) venv Python found
$venvPy = Join-Path $venv "Scripts\python.exe"
if (Test-Path $venvPy) {
    "{0,-26} $venvPy" -f "venv Python found" | Write-Host
    $pyver = & $venvPy -c "import sys;print('.'.join(map(str,sys.version_info[:3])))"
    "{0,-26} $pyver" -f "Python version" | Write-Host
} else {
    "{0,-26} missing" -f "venv Python found" | Write-Host
    "{0,-26} skip" -f "Python version" | Write-Host
}

# 4) requirements.txt present
if (Test-Path (Join-Path $root "requirements.txt")) {
    "{0,-26} found" -f "requirements.txt present" | Write-Host
} else {
    "{0,-26} missing" -f "requirements.txt present" | Write-Host
}

# 5) Git available + status
$gitVersion = git --version 2>$null
if ($LASTEXITCODE -eq 0) {
    "{0,-26} $gitVersion" -f "Git available" | Write-Host
} else {
    "{0,-26} missing" -f "Git available" | Write-Host
}

$gitStat = git status --porcelain 2>$null
if ($LASTEXITCODE -ne 0) {
    "{0,-26} git not initialized" -f "Git clean working tree" | Write-Host
} elseif ([string]::IsNullOrWhiteSpace($gitStat)) {
    "{0,-26} clean" -f "Git clean working tree" | Write-Host
} else {
    "{0,-26} pending changes" -f "Git clean working tree" | Write-Host
}

# 6) 0A_sorter_READY.py present
$sorter = Join-Path $root "scripts\phase0\0A_sorter_READY.py"
if (Test-Path $sorter) {
    "{0,-26} found" -f "0A_sorter_READY.py present" | Write-Host
} else {
    "{0,-26} missing" -f "0A_sorter_READY.py present" | Write-Host
}

# 7) Sorter runnable (--help)
if (Test-Path $venvPy -and (Test-Path $sorter)) {
    & $venvPy $sorter --help 1>$null 2>$null
    if ($LASTEXITCODE -eq 0) {
        "{0,-26} help shown" -f "Sorter runnable" | Write-Host
    } else {
        "{0,-26} error" -f "Sorter runnable" | Write-Host
    }
} else {
    "{0,-26} skip" -f "Sorter runnable" | Write-Host
}

Write-Host "`n==== ACCEPTANCE COMPLETE ===="
