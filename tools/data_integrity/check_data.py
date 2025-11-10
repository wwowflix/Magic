import os
import sqlite3

DB = r"E:\MAGIC\outputs\mydata.db"

if not os.path.exists(DB):
    print("⚠ No DB found:", DB)
    raise SystemExit(1)

con = sqlite3.connect(DB)
cur = con.cursor()
cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [r[0] for r in cur.fetchall()]
print("✅ DB Tables:", tables)

for t in ("google_trends", "reddit_scrape", "youtube_scrape"):
    try:
        cur.execute(f"SELECT COUNT(*) FROM {t}")
        print(f" - {t}: {cur.fetchone()[0]} rows")
    except Exception as e:
        print(f" - {t}: missing ({e})")

con.close()
