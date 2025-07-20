## 🔥 Reddit Scraper Integration

Run Reddit scraper:

    python trends_scraper.py --source reddit

Outputs:

    D:\MAGIC\scripts\outputs\reddit_scrape.csv

To ingest into the database:

    python ingest_csvs_to_db.py

Check table count:

    sqlite3 D:\MAGIC\scripts\trends_data.db "SELECT COUNT(*) FROM reddit;"

---

## 🔥 YouTube Scraper (Stub)

Run:

    python trends_scraper.py --source youtube

Outputs:

    D:\MAGIC\scripts\outputs\youtube_scrape.csv

To ingest into DB:

    python ingest_csvs_to_db.py

Check YouTube table:

    sqlite3 D:\MAGIC\scripts\trends_data.db "SELECT COUNT(*) FROM youtube;"
