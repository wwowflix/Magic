import pandas as pd, os
paths = ["outputs/google_trends.csv", "outputs/reddit_scrape.csv", "outputs/youtube_scrape.csv"]
for path in paths:
    if not os.path.exists(path): continue
    df = pd.read_csv(path)
    df.rename(columns={"Topic":"keyword"}, inplace=True)
    df.to_csv(path, index=False)
    print(f"✅ Standardized: {path}")
