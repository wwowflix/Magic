import sqlite3
import pandas as pd
import os

db_path = r'D:\MAGIC\outputs\zephyr_trends.db'

csv_files = {
    'google_trends': r'D:\MAGIC\scripts\google_trends_output.csv',
    'reddit': r'D:\MAGIC\outputs\reddit_scrape.csv',
    'youtube': r'D:\MAGIC\outputs\youtube_scrape.csv',
    'tiktok': r'D:\MAGIC\outputs\tiktok_scrape.csv'
}

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute('DROP TABLE IF EXISTS trends')
cursor.execute('''
CREATE TABLE trends (
    date TEXT,
    keyword TEXT,
    metric REAL,
    platform TEXT,
    author TEXT
)
''')

for platform, path in csv_files.items():
    if not os.path.exists(path):
        print(f"⚠️ File not found: {path}")
        continue

    print(f"✅ Loading {path}...")

    df = pd.read_csv(path)

    if "author" not in df.columns:
        df["author"] = "N/A"

    if "platform" not in df.columns:
        df["platform"] = platform

    cols = ['date', 'keyword', 'metric', 'platform', 'author']
    for col in cols:
        if col not in df.columns:
            df[col] = "N/A"

    df = df[cols]

    print(f"Loaded {len(df)} rows from {path}")
    df.to_sql("trends", conn, if_exists="append", index=False)

conn.close()
print("✅ All CSVs successfully ingested into SQLite database.")
