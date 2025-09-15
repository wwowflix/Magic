# -----------------------------------------------
# Run YouTube autocomplete scraper for many terms
# -----------------------------------------------

$keywords = @(
    "ai",
    "machine learning",
    "chatgpt",
    "midjourney",
    "data science"
)

foreach ($kw in $keywords) {
    Write-Host "Running scraper for keyword: $kw"
    python .\youtube_autocomplete_scraper.py $kw
}

# OPTIONAL: Open all CSVs after scraping
Get-ChildItem -Filter "youtube_autocomplete_output_*.csv" | ForEach-Object {
    Write-Host "Opening file: $($_.Name)"
    # Uncomment one of these if desired:
    # Start-Process notepad.exe $_.FullName
    # Start-Process excel.exe $_.FullName
}
