$pyFile = "D:\MAGIC\scripts\trends_scraper.py"

Write-Host "Scanning $pyFile for stray backslashes in triple-quoted docstrings..." -ForegroundColor Cyan

$content = Get-Content -Raw -Path $pyFile

# Replace any \"\"\" with """
$content = $content -replace '\\\"\\\"\\\"', '"""'

# Replace any stray backslash in front of single or double quotes
$content = $content -replace '\\(["''])', '$1'

Set-Content -Path $pyFile -Value $content -Encoding UTF8

Write-Host "✅ Stray backslashes removed from docstrings and quotes." -ForegroundColor Green
