# -*- coding: utf-8 -*-
#!/usr/bin/env python3

import pandas as pd
import sqlite3
import os

DB_PATH = r"D:\MAGIC\outputs\mydata.db"
OUTPUT_DIR = r"D:\MAGIC\outputs"

TABLES = {
    "google_trends.csv": "google_trends",
    "reddit_scrape.csv": "reddit",
    "youtube_scrape.csv": "youtube",
}

def ingest():
    conn = sqlite3.connect(DB_PATH)
    for csv_name, table in TABLES.items():
        csv_path = os.path.join(OUTPUT_DIR, csv_name)
        if os.path.exists(csv_path):
            print(f"Ingesting {csv_name} into table {table}...")
            df = pd.read_csv(csv_path)
            df.to_sql(table, conn, if_exists="replace", index=False)
        else:
            print(f"File not found: {csv_path}")
    conn.close()
    print("? All CSVs ingested successfully.")

if __name__ == "__main__":
    ingest()
