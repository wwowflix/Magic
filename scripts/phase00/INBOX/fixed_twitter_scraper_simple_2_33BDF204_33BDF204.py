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
import os
import certifi

os.environ["SSL_CERT_FILE"] = certifi.where()
import snscrape.modules.twitter as sntwitter
import csv

# Define query
query = "AI video since:2025-07-10 until:2025-07-19"
limit = 100

# Open CSV for writing
with open("outputs/twitter_trends.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["date", "username", "content", "url"])

    # Run scraper
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
        if i >= limit:
            break
        writer.writerow([tweet.date, tweet.user.username, tweet.content, tweet.url])

print("âœ… Scraped", limit, "tweets to outputs/twitter_trends.csv")
