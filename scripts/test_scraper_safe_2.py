# ✅ test_scraper_safe.py — Pure snscrape + pandas, NO numpy
import snscrape.modules.twitter as sntwitter
import pandas as pd

query = "AI tools since:2025-07-01 until:2025-07-20"
tweets = []

for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
    if i > 20:
        break
    tweets.append(
        {
            "date": tweet.date.strftime("%Y-%m-%d %H:%M"),
            "username": tweet.user.username,
            "content": tweet.content,
            "url": tweet.url,
        }
    )

df = pd.DataFrame(tweets)
df.to_csv("outputs/twitter_trends.csv", index=False)
print("✅ Twitter trends saved to outputs/twitter_trends.csv")
