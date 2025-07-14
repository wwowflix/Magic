# full_pipeline.ps1 — your all-in-one pipeline

# 1) Ensure we’re in the correct folder
Set-Location "D:\MAGIC\scripts"

# 2) Scrape all platforms
Write-Host "STEP 1 — Scraping Google Trends…"
python .\trends_scraper.py --source google

Write-Host "STEP 1 — Scraping Reddit…"
python .\trends_scraper.py --source reddit

Write-Host "STEP 1 — Scraping YouTube…"
python .\trends_scraper.py --source youtube

Write-Host "STEP 1 — Scraping TikTok…"
python .\trends_scraper.py --source tiktok

# 3) Load all CSVs into SQLite
Write-Host "STEP 2 — Ingesting CSVs into SQLite…"
python .\ingest_csvs_to_db.py

# 4) Run unit tests
Write-Host "STEP 3 — Running Unit Tests…"
.\run_tests.ps1

# 5) Launch Streamlit dashboard
Write-Host "STEP 4 — Launching Streamlit Dashboard…"
streamlit run .\dashboard.py
