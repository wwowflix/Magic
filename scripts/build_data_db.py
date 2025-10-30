# scripts/build_data_db.py
import sqlite3, os, time
from datetime import datetime

DB_PATH = r"E:\MAGIC\outputs\mydata.db"
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

schema_sql = """
PRAGMA journal_mode=WAL;
PRAGMA synchronous=NORMAL;

CREATE TABLE IF NOT EXISTS google_trends (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    keyword TEXT NOT NULL,
    region  TEXT,
    timeframe TEXT,
    score INTEGER,
    fetched_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_gt_keyword ON google_trends(keyword);
CREATE INDEX IF NOT EXISTS idx_gt_fetched ON google_trends(fetched_at);

CREATE TABLE IF NOT EXISTS reddit_scrape (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    keyword TEXT,
    subreddit TEXT,
    title TEXT,
    url TEXT,
    score INTEGER,
    comments INTEGER,
    posted_utc INTEGER,
    fetched_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_rs_keyword ON reddit_scrape(keyword);
CREATE INDEX IF NOT EXISTS idx_rs_sub ON reddit_scrape(subreddit);
CREATE INDEX IF NOT EXISTS idx_rs_posted ON reddit_scrape(posted_utc);

CREATE TABLE IF NOT EXISTS youtube_scrape (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    keyword TEXT,
    video_id TEXT,
    title TEXT,
    channel TEXT,
    views INTEGER,
    published TEXT,
    fetched_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_yt_keyword ON youtube_scrape(keyword);
CREATE INDEX IF NOT EXISTS idx_yt_published ON youtube_scrape(published);
"""

seed_sql = """
INSERT INTO google_trends (keyword, region, timeframe, score, fetched_at)
VALUES
 ('ai tools','US','now 7-d', 78, ?),
 ('ai tools','IN','now 7-d', 92, ?);

INSERT INTO reddit_scrape (keyword, subreddit, title, url, score, comments, posted_utc, fetched_at)
VALUES
 ('ai tools','MachineLearning','SOTA tool roundup','https://reddit.com/...', 120, 34, strftime('%s','now','-2 days'), ?),
 ('ai tools','ChatGPT','Best prompts list','https://reddit.com/...', 87, 15, strftime('%s','now','-1 day'), ?);

INSERT INTO youtube_scrape (keyword, video_id, title, channel, views, published, fetched_at)
VALUES
 ('ai tools','abcd1234','Top 10 AI Tools','TechDaily', 245000, date('now','-5 days'), ?),
 ('ai tools','wxyz9999','Automate your work with AI','BuildWithMe', 132000, date('now','-2 days'), ?);
"""


def main():
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with sqlite3.connect(DB_PATH) as con:
        con.executescript(schema_sql)
        con.executemany(
            "INSERT INTO google_trends (keyword, region, timeframe, score, fetched_at) VALUES (?,?,?,?,?)",
            [
                ("ai tools", "US", "now 7-d", 78, ts),
                ("ai tools", "IN", "now 7-d", 92, ts),
            ],
        )
        con.executemany(
            "INSERT INTO reddit_scrape (keyword, subreddit, title, url, score, comments, posted_utc, fetched_at) VALUES (?,?,?,?,?,?,?,?)",
            [
                (
                    "ai tools",
                    "MachineLearning",
                    "SOTA tool roundup",
                    "https://reddit.com/...",
                    120,
                    34,
                    int(time.time()) - 172800,
                    ts,
                ),
                (
                    "ai tools",
                    "ChatGPT",
                    "Best prompts list",
                    "https://reddit.com/...",
                    87,
                    15,
                    int(time.time()) - 86400,
                    ts,
                ),
            ],
        )
        con.executemany(
            "INSERT INTO youtube_scrape (keyword, video_id, title, channel, views, published, fetched_at) VALUES (?,?,?,?,?,?,?)",
            [
                (
                    "ai tools",
                    "abcd1234",
                    "Top 10 AI Tools",
                    "TechDaily",
                    245000,
                    "2025-10-19",
                    ts,
                ),
                (
                    "ai tools",
                    "wxyz9999",
                    "Automate your work with AI",
                    "BuildWithMe",
                    132000,
                    "2025-10-22",
                    ts,
                ),
            ],
        )
    print("DB ready at:", DB_PATH)


if __name__ == "__main__":
    main()
