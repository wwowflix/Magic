import pandas as pd

files = [
    "outputs/google_trends.csv",
    "outputs/reddit_scrape.csv",
    "outputs/youtube_scrape.csv",
    "outputs/tiktok_scrape.csv",
]

required_columns = {
    "outputs/google_trends.csv": ["term", "region", "score"],
    "outputs/reddit_scrape.csv": ["subreddit", "title", "score"],
    "outputs/youtube_scrape.csv": ["video_id", "title", "views"],
    "outputs/tiktok_scrape.csv": ["hashtag", "desc", "likes"],
}

for file in files:
    try:
        df = pd.read_csv(file)
        missing_cols = [col for col in required_columns[file] if col not in df.columns]
        if df.empty:
            print(f"⚠️ Empty file: {file}")
        elif missing_cols:
            print(f"❌ Missing columns in {file}: {missing_cols}")
        else:
            print(f"✅ All required columns present in {file}")
    except Exception as e:
        print(f"❌ Failed to read {file}: {e}")
