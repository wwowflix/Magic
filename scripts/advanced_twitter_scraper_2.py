# advanced_twitter_scraper_v3.py
import requests
from bs4 import BeautifulSoup
import time
import random
import json
from fake_useragent import UserAgent


class TwitterScraperV3:
    def __init__(self):
        self.ua = UserAgent()
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": self.ua.random,
                "Accept": "text/html,application/xhtml+xml",
                "Accept-Language": "en-US,en;q=0.5",
            }
        )

    def get_guest_token(self):
        """Get a guest token for API access"""
        try:
            response = self.session.post(
                "https://api.twitter.com/1.1/guest/activate.json",
                headers={
                    "Authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA"
                },
            )
            return response.json().get("guest_token")
        except:
            return None

    def scrape_tweets(self, query, max_tweets=10):
        """Hybrid scraping approach"""
        results = []

        # Method 1: Try mobile site first
        mobile_url = f"https://mobile.twitter.com/search?q={query}"
        try:
            print("Trying mobile site...")
            response = self.session.get(mobile_url)
            soup = BeautifulSoup(response.text, "html.parser")

            for tweet in soup.select("div.tweet"):
                content = tweet.select_one("div.tweet-text").get_text(strip=True)
                results.append({"content": content, "source": "mobile"})
                if len(results) >= max_tweets:
                    return results
                time.sleep(random.uniform(1, 3))
        except Exception as e:
            print(f"Mobile scrape failed: {str(e)[:100]}...")

        # Method 2: Try with guest token
        guest_token = self.get_guest_token()
        if guest_token:
            try:
                print("Trying API with guest token...")
                headers = {
                    "Authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
                    "x-guest-token": guest_token,
                }
                params = {
                    "q": query,
                    "count": min(max_tweets, 20),
                    "tweet_mode": "extended",
                }
                response = self.session.get(
                    "https://api.twitter.com/1.1/search/tweets.json",
                    headers=headers,
                    params=params,
                )
                for tweet in response.json().get("statuses", []):
                    results.append(
                        {
                            "content": tweet["full_text"],
                            "username": tweet["user"]["screen_name"],
                            "source": "api",
                        }
                    )
            except Exception as e:
                print(f"API with token failed: {str(e)[:100]}...")

        # Method 3: Fallback to HTML scraping
        if not results:
            try:
                print("Falling back to HTML scraping...")
                response = self.session.get(f"https://twitter.com/search?q={query}")
                soup = BeautifulSoup(response.text, "html.parser")

                for tweet in soup.select('article[data-testid="tweet"]'):
                    content = tweet.select_one("div[lang]").get_text(strip=True)
                    results.append({"content": content, "source": "html"})
                    if len(results) >= max_tweets:
                        break
                    time.sleep(random.uniform(2, 5))
            except Exception as e:
                print(f"HTML scrape failed: {str(e)[:100]}...")

        return results


if __name__ == "__main__":
    scraper = TwitterScraperV3()
    query = "python lang:en since:2025-07-01"

    print(f"Starting scrape for: {query}")
    tweets = scraper.scrape_tweets(query)

    with open("tweets.json", "w", encoding="utf-8") as f:
        json.dump(tweets, f, ensure_ascii=False, indent=2)

    print(f"Saved {len(tweets)} tweets to tweets.json")
