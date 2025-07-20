import snscrape.modules.twitter as sntwitter
import time
from random import randint

def safe_scrape(query, max_tweets=10, max_retries=3):
    tweets = []
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
        if i >= max_tweets:
            break
        tweets.append(tweet)
        time.sleep(randint(1, 3))  # Random delay
    return tweets

# Example usage (modify according to your script):
try:
    tweets = safe_scrape("python lang:en")
    for tweet in tweets:
        print(f"{tweet.date}: {tweet.content}")
except Exception as e:
    print(f"⚠️ Error: {str(e)}")
