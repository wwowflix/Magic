import sqlite3, os, pandas as pd
conn = sqlite3.connect("outputs/mydata.db")
files = {
    "google_trends":"outputs/google_trends.csv",
    "reddit":"outputs/reddit_scrape.csv",
    "youtube":"outputs/youtube_scrape.csv",
    "tiktok":"outputs/tiktok_scrape.csv"
}
for table, path in files.items():
    if os.path.exists(path):
        df = pd.read_csv(path)
        df.to_sql(table, conn, if_exists="replace", index=False)
        print(f"✅ Loaded: {table}")
conn.close()
