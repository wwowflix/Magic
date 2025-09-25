# -*- coding: utf-8 -*-
import sqlite3
import pandas as pd

db_path = r"D:\MAGIC\scripts\trends_data.db"
csv_path = r"D:\\MAGIC\\outputs\reddit_scrape.csv"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Read CSV with only relevant columns
df = pd.read_csv(csv_path, usecols=["date", "subreddit", "title"], encoding="utf-8-sig")

# Insert rows into reddit table
for _, row in df.iterrows():
    cursor.execute(
        "INSERT INTO reddit (date, subreddit, title) VALUES (?, ?, ?)",
        (row["date"], row["subreddit"], row["title"]),
    )

conn.commit()
print(f"OK Inserted {len(df)} rows into reddit table.")
conn.close()
