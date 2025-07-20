import snscrape.modules.twitter as sntwitter
import pandas as pd
from datetime import datetime

query = "AI tools OR ChatGPT OR Midjourney OR ElevenLabs lang:en since:2024-07-01"
limit = 100

tweets = []
for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
    if i >= limit:
        break
    tweets.append({
        'date': tweet.date,
        'content': tweet.content,
        'username': tweet.user.username,
        'url': tweet.url
    })

df = pd.DataFrame(tweets)
df.to_csv("outputs/twitter_scrape.csv", index=False)
print("✅ Saved Twitter trend data to outputs/twitter_scrape.csv")
