# scripts/twitter_scraper_simple.py

import pandas as pd
import snscrape.modules.twitter as sntwitter

query = "AI automation since:2023-01-01 until:2023-12-31"
max_tweets = 10
results = []

for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
    if i >= max_tweets:
        break
    results.append(
        {
            "date": tweet.date.strftime("%Y-%m-%d %H:%M"),
            "user": tweet.user.username,
            "content": tweet.content,
        }
    )

df = pd.DataFrame(results)
df.to_csv("outputs/twitter_scrape.csv", index=False, encoding="utf-8")
print("âœ… Twitter scrape complete â†’ outputs/twitter_scrape.csv")
