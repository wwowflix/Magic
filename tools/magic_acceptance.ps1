param(
    [string]$Root = "D:\MAGIC"
)

$EnvFile  = Join-Path $Root ".env"
$VenvDir  = Join-Path $Root "venv"
$PyExe    = Join-Path $VenvDir "Scripts\python.exe"
$Sorter   = Join-Path $Root "scripts\phase0\0A_sorter_READY.py"

$ok  = @{ sym = "✅"; fg = "Green" }
$bad = @{ sym = "❌"; fg = "Red"  }

function Show {
    param($name, $pass, $note = "")
    if ($pass) {
        $s = $ok.sym; $c = $ok.fg
    } else {
        $s = $bad.sym; $c = $bad.fg
    }
    Write-Host ("{0,-30} {1} {2}" -f $name, $s, $note) -ForegroundColor $c
}

function ShowWarn {
    param($name, $note = "")
    Write-Host ("{0,-30} ⚠️ {1}" -f $name, $note) -ForegroundColor Yellow
}

Write-Host "==== MAGIC ACCEPTANCE CHECK ====" -ForegroundColor Cyan

# 1) .env present
$envPresent = Test-Path $EnvFile
Show ".env present" $envPresent

# 2) venv
$venvExists = Test-Path $VenvDir
Show "venv folder exists" $venvExists

$pyExists = Test-Path $PyExe
Show "venv Python found" $pyExists

if ($pyExists) {
    try {
        $pyVersion = & $PyExe -c "import sys; print(sys.version.split()[0])"
        Show "Python version" $true $pyVersion
    } catch {
        Show "Python version" $false $_.Exception.Message
    }
}

# 3) requirements.txt
$reqFile = Join-Path $Root "requirements.txt"
Show "requirements.txt present" (Test-Path $reqFile)

# 4) Git
$gitDir = Join-Path $Root ".git"
if (Test-Path $gitDir) {
    try {
        $gitVersion = (git -C $Root --version)
        Show "Git available" $true $gitVersion
        $status = (git -C $Root status --porcelain)
        $clean = [string]::IsNullOrWhiteSpace($status)
        $gitNote = if ($clean) { "clean" } else { "pending changes" }
        Show "Git clean working tree" $clean $gitNote
    } catch {
        Show "Git available" $false $_.Exception.Message
    }
} else {
    ShowWarn "Git check" "No .git detected"
}

# 5) Sorter script
Show "0A_sorter_READY.py present" (Test-Path $Sorter)

if ((Test-Path $Sorter) -and $pyExists) {
    try {
        & $PyExe $Sorter --help | Out-Null
        Show "Sorter runnable" $true "help shown"
    } catch {
        Show "Sorter runnable" $false $_.Exception.Message
    }
} else {
    ShowWarn "Sorter runnable" "skip"
}

Write-Host "`n==== ACCEPTANCE COMPLETE ====" -ForegroundColor Cyan
