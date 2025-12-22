Write-Host "MAGIC Week-0 Import Audit Starting..."

$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD = "1"

$ScriptDir = "E:\MAGIC\scripts"
$Files = Get-ChildItem -LiteralPath $ScriptDir -Filter *.py

$Failures = @()
$Success  = @()

foreach ($file in $Files) {

    if ($file.Name -like "*magic_bak_week0*") { continue }

    $module = "scripts." + $file.BaseName
    Write-Host ("Importing " + $module + " ...") -NoNewline

    $pyCode = "import importlib, sys; importlib.import_module('" + $module + "')"

    python -c $pyCode

    if ($LASTEXITCODE -eq 0) {
        Write-Host " OK"
        $Success += $module
    }
    else {
        Write-Host " FAIL"
        $Failures += $module
    }
}

Write-Host ""
Write-Host "==============================================="
Write-Host "WEEK-0 IMPORT AUDIT SUMMARY"
Write-Host "==============================================="

$total = $Success.Count + $Failures.Count

if ($total -eq 0) {
    Write-Host "ERROR: No modules processed!"
}
else {
    $passed  = $Success.Count
    $failed  = $Failures.Count
    $percent = [math]::Round(($passed / $total) * 100, 2)

    Write-Host ("Total modules: " + $total)
    Write-Host ("Passed: " + $passed)
    Write-Host ("Failed: " + $failed)
    Write-Host ("Progress: " + $percent + " % complete")

    Write-Host ""
    Write-Host "Remaining failures:"

    if ($Failures.Count -eq 0) {
        Write-Host "NONE - Week 0 Import Layer is COMPLETE!"
    }
    else {
        foreach ($f in $Failures) {
            Write-Host (" - " + $f)
        }
    }
}

Write-Host ""
Write-Host "Week-0 Audit Complete."
