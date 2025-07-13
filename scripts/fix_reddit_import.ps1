# fix_reddit_import.ps1
# ---------------------
# Scans trends_scraper.py for \import praw and replaces it with import praw

$pyFile = "D:\MAGIC\scripts\trends_scraper.py"

if (Test-Path $pyFile) {
    Write-Host "Patching $pyFile..." -ForegroundColor Cyan

    $content = Get-Content $pyFile -Raw
    $content = $content -replace '\\import praw','import praw'

    Set-Content -Path $pyFile -Value $content -Encoding UTF8

    Write-Host "✅ Removed stray backslash from import statement." -ForegroundColor Green
} else {
    Write-Host "File not found: $pyFile" -ForegroundColor Red
}
