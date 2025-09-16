import pandas as pd
import sqlite3
import os

db_path = os.path.join("outputs", "mydata.db")

# Ensure outputs directory exists
os.makedirs("outputs", exist_ok=True)

conn = sqlite3.connect(db_path)

file_table_map = {
    "google_trends.csv": "google_trends",
    "reddit_scrape.csv": "reddit_scrape",
    "youtube_scrape.csv": "youtube_scrape",
    "tiktok_scrape.csv": "tiktok_scrape",
}

for csv_filename, table_name in file_table_map.items():
    csv_path = os.path.join("outputs", csv_filename)
    if os.path.exists(csv_path) and os.path.getsize(csv_path) > 0:
        try:
            print(f"Reading: {csv_path}")
            df = pd.read_csv(csv_path)
            if df.empty:
                print(f"[SKIPPED] {table_name} is empty.")
                continue
            df.to_sql(table_name, conn, if_exists="replace", index=False)
            print(f"[OK] Loaded {csv_filename} into table {table_name}")
        except Exception as e:
            import traceback

            print(f"[ERROR] Failed to process {csv_path}: {e}")
            traceback.print_exc()
    else:
        print(f"[SKIPPED] No data in {csv_filename}")

conn.close()
print("[DONE] Ingestion complete.")
