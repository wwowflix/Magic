@"
<#
.SYNOPSIS
    Executes all *_READY.py scripts in a given Phase 11 module and logs output.
.DESCRIPTION
    - Takes a module letter (e.g. B, C, D…) as a parameter.
    - Discovers each READY script under scripts/phase11/module_<Module>.
    - Ensures a log directory exists.
    - Runs them one by one, capturing stdout/stderr into individual log files.
    - Writes a summary.tsv with Script and Status columns.
    - Prints colored status to the console.
.PARAMETER Module
    The Phase 11 module letter to run (e.g. "B").
.EXAMPLE
    .\run_phase11_module.ps1 -Module B
#>

param(
    [Parameter(Mandatory)]
    [ValidatePattern('^[A-Z]$')]
    [string]$Module
)

# Paths
$scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Definition
$moduleDir  = Join-Path $scriptRoot "scripts\phase11\module_$Module"
$logDir     = Join-Path $scriptRoot "outputs\logs\phase11_module_$Module"

# Prep
if (-Not (Test-Path $moduleDir)) {
    Write-Error "Module directory not found: $moduleDir"
    exit 1
}
New-Item -ItemType Directory -Path $logDir -Force | Out-Null

# Summary collection
$summary = @()

# Run each script
Get-ChildItem -Path $moduleDir -Filter '*_READY.py' -File | Sort-Object Name | ForEach-Object {
    $scriptName = $_.Name
    $scriptPath = $_.FullName
    $logPath    = Join-Path $logDir ($scriptName + '.log')
    $timestamp  = (Get-Date).ToString('s')

    Write-Host "[$timestamp] → Running $scriptName" -NoNewline

    # Execute and capture
    $proc = Start-Process python -ArgumentList "`"$scriptPath`"" `
                  -RedirectStandardOutput $logPath `
                  -RedirectStandardError  $logPath `
                  -NoNewWindow -Wait -PassThru

    if ($proc.ExitCode -eq 0) {
        Write-Host "  ✓ $scriptName executed successfully."
        $status = "OK"
    } else {
        Write-Host "  ✗ $scriptName FAILED (exit $($proc.ExitCode)). See log: $logPath"
        $status = "ERROR"
    }

    $summary += [PSCustomObject]@{
        Script = $scriptName
        Status = $status
    }
}

# Write summary.tsv
$summaryPath = Join-Path $logDir 'summary.tsv'
"Script`tStatus" | Out-File -FilePath $summaryPath -Encoding UTF8
$summary | ForEach-Object { "$($_.Script)`t$($_.Status)" } | Out-File -FilePath $summaryPath -Append -Encoding UTF8

Write-Host "`nSummary written to $summaryPath"

# Exit with code if any failures
if ($summary.Status -contains 'ERROR') { exit 1 } else { exit 0 }
"@ | Set-Content -Path .\run_phase11_module.ps1 -Encoding UTF8
