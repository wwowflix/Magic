param(
    [Parameter(Mandatory)]
    [ValidatePattern('^[A-Z]$')]
    [string]$Module
)

# Paths
$scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Definition
$moduleDir  = Join-Path $scriptRoot "scripts\phase11\module_$Module"
$logDir     = Join-Path $scriptRoot "outputs\logs\phase11_module_$Module"

# Verify module folder
if (-not (Test-Path $moduleDir)) {
    Write-Error "Module directory not found: $moduleDir"
    exit 1
}

# Ensure log folder exists
New-Item -ItemType Directory -Path $logDir -Force | Out-Null

$summary = @()

# Run each *_READY.py
Get-ChildItem -Path $moduleDir -Filter '*_READY.py' -File |
  Sort-Object Name |
  ForEach-Object {
    $name    = $_.Name
    $path    = $_.FullName
    $logFile = Join-Path $logDir ($name + '.log')
    $ts      = (Get-Date).ToString('s')

    Write-Host "[$ts] → Running $name"

    # Redirect both stdout & stderr
    & python $path > $logFile 2>&1
    $exitCode = $LASTEXITCODE

    if ($exitCode -eq 0) {
        Write-Host "  ✓ $name succeeded."
        $status = "OK"
    } else {
        Write-Host "  ✗ $name failed (exit $exitCode). See $logFile"
        $status = "ERROR"
    }

    $summary += [PSCustomObject]@{
        Script = $name
        Status = $status
    }
  }

# Emit summary.tsv in one step
$summaryPath = Join-Path $logDir 'summary.tsv'
$header     = "Script`tStatus"
$entries    = $summary | ForEach-Object { "$($_.Script)`t$($_.Status)" }

@($header) + $entries |
    Out-File -FilePath $summaryPath -Encoding UTF8

Write-Host "`nSummary written to $summaryPath"

# Fail if any module script errored
if ($summary.Status -contains 'ERROR') { exit 1 } else { exit 0 }
