# suppress_chrome_warnings.ps1

# List of your scraper files
$pyFiles = @(
    "D:\MAGIC\scripts\trends_scraper.py",
    "D:\MAGIC\scripts\tiktok_xhr_scraper.py"
)

foreach ($pyFile in $pyFiles) {
    # Only append if driver.quit is not already there
    if (-not (Select-String -Path $pyFile -Pattern 'driver\.quit')) {
        Add-Content $pyFile ""
        Add-Content $pyFile "# Cleanly close Chrome to avoid WinError 6 in undetected_chromedriver"
        Add-Content $pyFile "try:"
        Add-Content $pyFile "    driver.quit()"
        Add-Content $pyFile "except Exception:"
        Add-Content $pyFile "    pass"
        Write-Host "Appended driver.quit() cleanup to $($pyFile | Split-Path -Leaf)"
    }
    else {
        Write-Host "$($pyFile | Split-Path -Leaf) already has driver.quit() cleanup"
    }
}

Write-Host "`n✅ Cleanup logic appended. Rerun your scrapers to verify no more warnings." -ForegroundColor Cyan
