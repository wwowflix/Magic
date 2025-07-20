# scripts/twitter_scraper_simple.py

import snscrape.modules.twitter as sntwitter
import pandas as pd
from datetime import datetime

query = "AI automation since:2023-01-01 until:2023-12-31"
max_tweets = 10
results = []

for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
    if i >= max_tweets:
        break
    results.append({
        "date": tweet.date.strftime("%Y-%m-%d %H:%M"),
        "user": tweet.user.username,
        "content": tweet.content
    })

df = pd.DataFrame(results)
df.to_csv("outputs/twitter_scrape.csv", index=False, encoding="utf-8")
print("✅ Twitter scrape complete → outputs/twitter_scrape.csv")
