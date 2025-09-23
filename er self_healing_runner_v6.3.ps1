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
    if (-Not (Test-Path $ManifestPath)) {
        return $false
    }
    try {
        $manifest = Get-Content $ManifestPath -Raw | ConvertFrom-Json
        return ($manifest.phases -contains $Phase)
    }
    catch {
        Write-Warning "Could not parse manifest at $ManifestPath. Assuming phase not complete."
        return $false
    }
}

function Update-PhaseManifest {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)] [string]$ManifestPath,
        [Parameter(Mandatory)] [string]$Phase
    )

    # Load or reinitialize
    if (Test-Path $ManifestPath) {
        try {
            $existing = Get-Content $ManifestPath -Raw | ConvertFrom-Json
        }
        catch {
            Write-Warning "Invalid JSON in manifest. Reinitializing."
            $existing = $null
        }
    }
    else {
        $existing = $null
    }

    # Normalize to array
    if ($existing -is [System.Collections.IEnumerable] -and $existing -isnot [string]) {
        $phases = @($existing)
    }
    elseif ($existing -and $existing.psobject.Properties.Name -contains 'phases') {
        $phases = @($existing.phases)
    }
    else {
        $phases = @()
    }

    # Add this phase
    if ($phases -notcontains $Phase) {
        $phases += $Phase
    }

    # Write back
    $manifestObj = [PSCustomObject]@{ phases = $phases }
    try {
        $manifestObj |
          ConvertTo-Json -Depth 10 |
          Set-Content -Path $ManifestPath
        Write-Host "Updated manifest: phases = $($phases -join ', ')"
    }
    catch {
        Write-Error "Failed to write manifest to ${ManifestPath}: $_"
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

# === YOUR PHASES/MODULES/SCRIPTS ===
$ScriptRuns = @(
    @{ Phase  = 'phase10'; Module = 'module_A'; Script = '10A_title_meta_writing.ps1'; Help = 'Generate title & meta.' },
    @{ Phase  = 'phase20'; Module = 'module_B'; Script = '20B_meta_remediation.ps1'; Help = 'Remediate meta data.' }
)

# Main loop
foreach ($run in $ScriptRuns) {
    if (-not (Test-PhaseComplete -ManifestPath $PhaseManifestPath -Phase $run.Phase)) {
        Write-Host "=== Applying $($run.Phase) : $($run.Module) ==="
        Apply-Remediation -FilePath $run.Script
        Update-PhaseManifest -ManifestPath $PhaseManifestPath -Phase $run.Phase
    }
    else {
        Write-Host "Skipping $($run.Phase): already completed."
    }
}
