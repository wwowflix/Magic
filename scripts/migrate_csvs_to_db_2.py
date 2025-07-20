# -*- coding: utf-8 -*-
import sqlite3
import pandas as pd
import glob
import os

# Path to your DB
db_path = r"D:\MAGIC\outputs\zephyr_trends.db"

# Connect
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Folder with all CSVs
csv_dir = r"D:\MAGIC\outputs"

# Find all CSV files
csv_files = glob.glob(os.path.join(csv_dir, "*.csv"))

total_rows_inserted = 0

for file in csv_files:
    # Infer platform from filename
    base = os.path.basename(file)
    if "google_trends" in base:
        platform = "google_trends"
    elif "youtube_autocomplete" in base:
        platform = "youtube_autocomplete"
    elif "reddit" in base:
        platform = "reddit"
    elif "tiktok" in base:
        platform = "tiktok"
    elif "amazon" in base:
        platform = "amazon"
    else:
        platform = "unknown"

    print(f"Processing: {file} (platform={platform})")

    try:
        df = pd.read_csv(file)
    except Exception as e:
        print(f"? Could not read {file}: {e}")
        continue

    if df.empty:
        print(f"Skipping empty file: {file}")
        continue

    # Ensure required columns exist
    if not set(["date", "keyword", "metric"]).issubset(df.columns):
        print(f"Skipping file missing required columns: {file}")
        continue

    # Add platform column if missing
    if "platform" not in df.columns:
        df["platform"] = platform

    # Insert rows into DB
    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO trends (date, keyword, platform, metric)
            VALUES (?, ?, ?, ?)
        """, (
            str(row["date"]),
            str(row["keyword"]),
            str(row["platform"]),
            float(row["metric"]) if not pd.isna(row["metric"]) else None
        ))
        total_rows_inserted += 1

conn.commit()
conn.close()

print(f"[OK] Migration complete. Rows inserted: {total_rows_inserted}")



