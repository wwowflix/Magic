# auto_fix_trends_and_tiktok.ps1
# Backs up and patches your scraper scripts to use BOM-safe JSON loading,
# ensures Chrome driver cleanup, and reports completion.

# 1) Files to patch
$pyFiles = @(
    "D:\MAGIC\scripts\trends_scraper.py",
    "D:\MAGIC\scripts\tiktok_xhr_scraper.py"
)

foreach ($pyFile in $pyFiles) {
    # Backup original if not already
    $bak = "$pyFile.bak"
    if (-not (Test-Path $bak)) {
        Copy-Item -Path $pyFile -Destination $bak -Force
        Write-Host "Backed up $($pyFile | Split-Path -Leaf) → $($bak | Split-Path -Leaf)"
    }

    # Read and patch JSON open() calls to use utf-8-sig
    $content = Get-Content -Path $pyFile
    $patched = $content | ForEach-Object {
        if ($_ -match 'with\s+open\s*\(') {
            # Extract path argument inside open(...)
            if ($_ -match 'with\s+open\s*\(\s*([^) ,]+)') {
                $pathArg = $matches[1]
                # Reconstruct the line with correct parameters
                $suffix = ''
                if ($_ -match '\)\s*as\s+f') {
                    $suffix = $_.Substring($_.IndexOf(')') + 1)
                }
                "with open($pathArg, `"r`", encoding=`"utf-8-sig`")$suffix"
            } else {
                $_
            }
        } else {
            $_
        }
    }

    # Write the patched file back
    $patched | Set-Content -Path $pyFile -Encoding UTF8
    Write-Host "Patched $($pyFile | Split-Path -Leaf) for BOM-safe loading."

    # Append driver.quit cleanup if missing
    if (-not (Select-String -Path $pyFile -Pattern 'driver\.quit')) {
        Add-Content -Path $pyFile -Value ""
        Add-Content -Path $pyFile -Value "# Cleanup Chrome driver handle to avoid WinError 6"
        Add-Content -Path $pyFile -Value "try:"
        Add-Content -Path $pyFile -Value "    driver.quit()"
        Add-Content -Path $pyFile -Value "except:"
        Add-Content -Path $pyFile -Value "    pass"
        Write-Host "Appended driver.quit() cleanup to $($pyFile | Split-Path -Leaf)"
    }
}

Write-Host "`n✅ Auto-patch complete. Now you can rerun your scrapers or tests." -ForegroundColor Cyan
