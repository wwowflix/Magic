# discover_tiktok_selectors.ps1

# 1. Launch Chrome at your TikTok video URL
$videoUrl = "https://www.tiktok.com/@someuser/video/XXXXXXXXXXXX"
Start-Process "chrome.exe" $videoUrl

# 2. Prompt user to inspect manually
Write-Host ""
Write-Host "?? Please inspect the TikTok video description element in DevTools."
Write-Host "?? Once copied, paste your CSS selector below and press Enter."
Write-Host ""

# 3. Read selector from user
$selector = Read-Host "Paste your CSS selector"

# 4. Replace DESC_SELECTOR in Python file
$pyFile = "D:\MAGIC\scripts\tiktok_scraper.py"

(Get-Content $pyFile) -replace 'DESC_SELECTOR\s*=.*', "DESC_SELECTOR = `"$selector`"" | Set-Content $pyFile

Write-Host ""
Write-Host "? DESC_SELECTOR has been updated in $pyFile"
