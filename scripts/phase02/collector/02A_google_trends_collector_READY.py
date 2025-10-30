import os, sqlite3, time
from datetime import datetime, timezone

ROOT = r"E:\MAGIC"
DB = os.path.join(ROOT, "outputs", "mydata.db")
os.makedirs(os.path.dirname(DB), exist_ok=True)

con = sqlite3.connect(DB)
cur = con.cursor()
cur.execute(
    """
CREATE TABLE IF NOT EXISTS google_trends(
  keyword TEXT NOT NULL,
  region  TEXT NOT NULL,
  ts      TEXT NOT NULL,
  value   INTEGER NOT NULL
)
"""
)

now = datetime.now(timezone.utc).isoformat()
rows = [
    ("ai", "US", now, 63),
    ("chatgpt", "US", now, 71),
    ("python", "US", now, 54),
    ("streamlit", "US", now, 37),
    ("ai", "GB", now, 48),
    ("chatgpt", "GB", now, 58),
    ("python", "GB", now, 46),
    ("streamlit", "GB", now, 32),
]

cur.executemany(
    "INSERT INTO google_trends(keyword,region,ts,value) VALUES(?,?,?,?)", rows
)
con.commit()
con.close()
print(f"Inserted {len(rows)} rows into google_trends at {now}")
