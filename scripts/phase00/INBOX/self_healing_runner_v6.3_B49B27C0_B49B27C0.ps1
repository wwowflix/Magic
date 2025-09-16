<#
.SYNOPSIS
    Self-healing runner to apply remediation scripts in phases and update manifest.
#>

param(
    [string]$PhaseManifestPath = 'phase_manifest.json'
)

function Test-PhaseComplete {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)] [string]$ManifestPath,
        [Parameter(Mandatory)] [string]$Phase
    )
    if (-Not (Test-Path $ManifestPath)) { return $false }
    $manifest = Get-Content $ManifestPath -Raw | ConvertFrom-Json
    return $manifest.phases -contains $Phase
}

function Update-PhaseManifest {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)] [string]$ManifestPath,
        [Parameter(Mandatory)] [string]$Phase
    )
    if (Test-Path $ManifestPath) {
        $manifest = Get-Content $ManifestPath -Raw | ConvertFrom-Json
    }
    else {
        $manifest = [PSCustomObject]@{ phases = @() }
    }
    if ($manifest.phases -notcontains $Phase) {
        $manifest.phases += $Phase
        $manifest | ConvertTo-Json -Depth 10 | Set-Content $ManifestPath
    }
}

function Apply-Remediation {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)] [string]$FilePath
    )
    Write-Host "Running remediation script: $FilePath"
    try {
        if (Test-Path $FilePath) {
            & $FilePath
            Write-Host "Successfully executed $FilePath"
        }
        else {
            Write-Warning "Script file not found: $FilePath"
        }
    }
    catch {
        Write-Error "Error executing ${FilePath}: $_"
    }
}

# Define your phases/modules/scripts here:
$ScriptRuns = @(
    @{ Phase  = 'phase10'; Module = 'module_A'; Script = '10A_title_meta_writing.ps1'; Help = 'Generate title & meta.' },
    @{ Phase  = 'phase20'; Module = 'module_B'; Script = '20B_meta_remediation.ps1'; Help = 'Remediate meta data.' }
)

# Main execution loop
foreach ($run in $ScriptRuns) {
    if (-not (Test-PhaseComplete -ManifestPath $PhaseManifestPath -Phase $run.Phase)) {
        Write-Host "=== Applying $($run.Phase) : $($run.Module) ==="
        Apply-Remediation -FilePath $run.Script
        Update-PhaseManifest -ManifestPath $PhaseManifestPath -Phase $run.Phase
    }
    else {
        Write-Host "$($run.Phase) already completed. Skipping."
    }
}
