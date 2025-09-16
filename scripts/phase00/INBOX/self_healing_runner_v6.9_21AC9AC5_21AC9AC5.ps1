function Run-Script {
    param(
        [string]$ScriptPath,
        [string]$LogFile
    )

    # Ensure log directory exists
    $logDir = Split-Path $LogFile
    if (!(Test-Path $logDir)) {
        New-Item -ItemType Directory -Path $logDir -Force | Out-Null
    }

    try {
        Write-Host "▶ Running: $(Split-Path $ScriptPath -Leaf)"
        # Run Python script and log both stdout and stderr
        & python "$ScriptPath" *>> "$LogFile"
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Success: $(Split-Path $ScriptPath -Leaf)"
        }
        else {
            Write-Warning "⚠ Script returned non-zero exit code!"
        }
    }
    catch {
        Write-Warning "❌ Error running script: $($_.Exception.Message)"
    }
}
