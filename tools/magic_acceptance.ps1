param(
    [string]$Root = "E:\MAGIC"
)

Write-Host "Running MAGIC Acceptance Scan..." -ForegroundColor Cyan

# Basic readiness checks (you can expand later)
$checks = @(
    @{ Step=1; Check="Root folder exists";                     Test={ Test-Path $Root }; Notes="" },
    @{ Step=2; Check="venv folder exists";                     Test={ Test-Path "$Root\venv" }; Notes="" },
    @{ Step=3; Check="scripts folder exists";                  Test={ Test-Path "$Root\scripts" }; Notes="" },
    @{ Step=4; Check="tools folder exists";                    Test={ Test-Path "$Root\tools" }; Notes="" },
    @{ Step=5; Check="Notion sync config exists";              Test={ Test-Path "$Root\.env" }; Notes="Check NOTION keys" },
    @{ Step=6; Check="pytest.ini exists";                      Test={ Test-Path "$Root\pytest.ini" }; Notes="" }
)

# Evaluate
$results = $checks | ForEach-Object {
    $result = Invoke-Command -ScriptBlock $_.Test
    [PSCustomObject]@{
        Step   = $_.Step
        Check  = $_.Check
        Status = if ($result) { "✅" } else { "❌" }
        Notes  = $_.Notes
    }
}

# Display
$results | Format-Table -AutoSize
