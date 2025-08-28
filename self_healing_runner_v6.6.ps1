param(
    [string]$ManifestPath = "phase_manifest.json",
    [int]   $MaxRetries   = 2
)

Write-Host "=== Starting Self-Healing Runner v6.6 ==="

# Prepare output dirs
$logRoot = "outputs\logs";  $sumRoot = "outputs\summaries"
New-Item -ItemType Directory -Force -Path $logRoot, $sumRoot | Out-Null

# Summary file
$ts          = Get-Date -Format 'yyyyMMdd_HHmmss'
$summaryFile = Join-Path $sumRoot "runner_summary_$ts.txt"

# Load manifest as an array
if (-not (Test-Path $ManifestPath)) { throw "Manifest missing: $ManifestPath" }
$entries = @(Get-Content $ManifestPath -Raw | ConvertFrom-Json)

function Apply-Remediation {
    param($err, $scriptPath)
    switch -Regex ($err) {
      'FileNotFoundError'    { 'placeholder' | Out-File (Join-Path (Split-Path $scriptPath) 'dummy_input.txt') -Encoding UTF8; return $true }
      'UnicodeEncodeError'   { (Get-Content $scriptPath) -replace '[^\x00-\x7F]', '' | Set-Content $scriptPath; return $true }
      'ImportError|ModuleNotFoundError' {
          if (Test-Path 'requirements.txt') { pip install -r requirements.txt; return $true }
      }
      default { return $false }
    }
}

foreach ($e in $entries) {
    if (-not $e.PSObject.Properties.Match('FinalFilename') -or [string]::IsNullOrWhiteSpace($e.FinalFilename)) {
        Write-Host "↷ Skipping entry missing FinalFilename" -ForegroundColor DarkGray; continue
    }
    $script = $e.FinalFilename
    if (-not (Test-Path $script)) {
        Write-Host "⚠️  Script not found, skipping: $script" -ForegroundColor Yellow; continue
    }
    $phase = $e.PhaseNumber; $mod = $e.Module
    $dir   = Join-Path $logRoot "phase${phase}_module_${mod}"
    New-Item -ItemType Directory -Force -Path $dir | Out-Null
    $log   = Join-Path $dir ((Split-Path $script -Leaf) + '.log')

    Write-Host "`n>>> Running $script"
    $attempt = 1; $success = $false

    while ($attempt -le $MaxRetries -and -not $success) {
        try {
            python $script *>&1 | Tee-Object -FilePath $log
            if ($LASTEXITCODE -eq 0) {
                Write-Host "✔ Success on attempt $attempt"
                "$phase`t$mod`t$(Split-Path $script -Leaf)`tSuccess" | Add-Content $summaryFile
                $success = $true
            } else { throw "Exit code $LASTEXITCODE" }
        } catch {
            $msg = $_.Exception.Message
            Write-Host "✖ Error on attempt ${attempt}: ${msg}"
            if (Apply-Remediation $msg $script) {
                Write-Host "…remediated, retrying"
            } else {
                Write-Host "No auto-fix available"
                "$phase`t$mod`t$(Split-Path $script -Leaf)`tFailure:$msg" | Add-Content $summaryFile
                break
            }
        }
        $attempt++
    }
    if (-not $success) { Write-Host "❌ Final failure: $script" }
}

Write-Host "`n=== Runner complete ==="
Write-Host "Logs in:    $logRoot"
Write-Host "Summary in: $summaryFile"
