Write-Host "`n🚀 Running Phase 2: Trend Engine Pipeline`n" -ForegroundColor Cyan

$base = "D:\MAGIC"
$py = "python"  # or full path like "C:\Python\python.exe"

# Step 1: Scrape from each platform (skip if file missing)
$trendScripts = @(
    "scripts\trends\google_trends_scraper.py",
    "scripts\trends\reddit_scraper.py",
    "scripts\trends\youtube_scraper.py",
    "scripts\trends\tiktok_scraper.py"
)

foreach ($script in $trendScripts) {
    $fullPath = Join-Path $base $script
    if (Test-Path $fullPath) {
        Write-Host "▶️ Running: $script"
        & $py $fullPath
    } else {
        Write-Host "⏭️ Skipped (not found): $script"
    }
}

# Step 2: Merge all CSVs
$mergeScript = Join-Path $base "scripts\trends\trends_merge.py"
if (Test-Path $mergeScript) {
    Write-Host "🔗 Merging trend sources..."
    & $py $mergeScript
}

# Step 3: Rank trends
$rankScript = Join-Path $base "scripts\trends\trend_ranker.py"
if (Test-Path $rankScript) {
    Write-Host "📊 Ranking trends..."
    & $py $rankScript
}

# Step 4: Save final output
$saveScript = Join-Path $base "scripts\trends\save_trends.py"
if (Test-Path $saveScript) {
    Write-Host "💾 Saving top trends to CSV..."
    & $py $saveScript
}

Write-Host "`n✅ Trend Engine Pipeline Complete." -ForegroundColor Green
