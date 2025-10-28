# scripts/collect/google_trends_fetcher.py
# Usage:
#   python scripts/collect/google_trends_fetcher.py --keywords "ai tools" chatgpt python --regions US IN --timeframe "now 7-d"
import argparse, sqlite3, os
from datetime import datetime
from pytrends.request import TrendReq

DB_PATH = r"E:\MAGIC\outputs\mydata.db"

def ensure_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    with sqlite3.connect(DB_PATH) as con:
        con.executescript("""
        PRAGMA journal_mode=WAL;
        CREATE TABLE IF NOT EXISTS google_trends(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            keyword TEXT NOT NULL,
            region TEXT,
            timeframe TEXT,
            score INTEGER,
            fetched_at TEXT NOT NULL
        );
        CREATE INDEX IF NOT EXISTS idx_gt_keyword ON google_trends(keyword);
        CREATE INDEX IF NOT EXISTS idx_gt_fetched ON google_trends(fetched_at);
        """)

def upsert_trends(keywords, regions, timeframe):
    pytrends = TrendReq(hl='en-US', tz=0)
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    rows = []
    for kw in keywords:
        for region in regions:
            pytrends.build_payload([kw], timeframe=timeframe, geo=region)
            df = pytrends.interest_over_time()
            if df is None or df.empty:
                continue
            score = int(df[kw].iloc[-1])  # most recent point
            rows.append((kw, region, timeframe, score, ts))
    if not rows:
        return 0
    with sqlite3.connect(DB_PATH, check_same_thread=False) as con:
        con.executemany(
            "INSERT INTO google_trends(keyword, region, timeframe, score, fetched_at) VALUES(?,?,?,?,?)",
            rows
        )
    return len(rows)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--keywords", nargs="+", required=True)
    p.add_argument("--regions", nargs="+", default=["US"])
    p.add_argument("--timeframe", default="now 7-d")
    args = p.parse_args()
    ensure_db()
    n = upsert_trends(args.keywords, args.regions, args.timeframe)
    print(f"[google_trends] wrote {n} rows")

if __name__ == "__main__":
    main()
