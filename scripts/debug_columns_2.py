import pandas as pd, os
files = ["outputs/google_trends.csv", "outputs/reddit_scrape.csv", "outputs/youtube_scrape.csv", "outputs/tiktok_scrape.csv"]
for f in files:
    if os.path.exists(f):
        try:
            df = pd.read_csv(f)
            print(f"\n🧾 {f}: {list(df.columns)}")
        except Exception as e:
            print(f"❌ Error reading {f}: {e}")
