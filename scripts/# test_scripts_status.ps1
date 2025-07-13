@'
# test_scripts_status.ps1

# Automatically test which Python scripts in D:\MAGIC\scripts are working
$tests = @(
    @{ File = 'trends_scraper.py';        Args = '--help'    },
    @{ File = 'orchestrator.py';          Args = '--dry-run' },
    @{ File = 'tiktok_xhr_scraper.py';    Args = ''          }
)

Write-Host "`n🚀 Testing all scripts in D:\MAGIC\scripts..." -ForegroundColor Cyan
Push-Location "D:\MAGIC\scripts"

$results = foreach ($t in $tests) {
    $path = ".\$($t.File)"
    if (-not (Test-Path $path)) {
        [PSCustomObject]@{
            Script  = $t.File
            Status  = 'Not Found'
            Command = ''
        }
        continue
    }

    $cmd = if ($t.Args) { "python $path $($t.Args)" } else { "python $path" }
    Write-Host "Testing $($t.File) with '$($t.Args)'..." -NoNewline
    Invoke-Expression $cmd | Out-Null
    $pass = if ($LASTEXITCODE -eq 0) { 'Working' } else { 'Failed' }
    Write-Host " $pass"

    [PSCustomObject]@{
        Script  = $t.File
        Status  = $pass
        Command = $cmd
    }
}

Pop-Location

# Display results
$results | Format-Table -AutoSize

Write-Host "`nAll script tests complete." -ForegroundColor Cyan
'@ | Set-Content -Path test_scripts_status.ps1 -Encoding UTF8

Write-Host "✅ Created test_scripts_status.ps1. Now run `.\test_scripts_status.ps1`"
