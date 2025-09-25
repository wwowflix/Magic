import time
from fake_useragent import UserAgent
import requests


# Add retry logic
def safe_request(url, max_retries=3):
    ua = UserAgent()
    for i in range(max_retries):
        try:
            response = requests.get(url, headers={"User-Agent": ua.random})
            response.raise_for_status()
            return response
        except Exception:
            if i == max_retries - 1:
                raise
            time.sleep(2**i)


# Original script content follows:
import pandas as pd
import snscrape.modules.twitter as sntwitter

query = "AI OR artificial intelligence lang:en"
limit = 50

tweets = []

for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
    if i >= limit:
        break
    tweets.append(
        {
            "date": tweet.date,
            "username": tweet.user.username,
            "content": tweet.content,
            "url": tweet.url,
        }
    )

df = pd.DataFrame(tweets)
df.to_csv("outputs/twitter_scrape.csv", index=False)
print("? Saved Twitter scrape to outputs/twitter_scrape.csv")
