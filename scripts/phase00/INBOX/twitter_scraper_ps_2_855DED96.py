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
                "Accept": "*/*",
                "Accept-Language": "en-US,en;q=0.9",
                "Referer": "https://twitter.com/",
                "DNT": "1",
                "Connection": "keep-alive",
            }
        )

    def get_guest_token(self):
        """Get a guest token for API access"""
        try:
            response = self.session.post(
                "https://api.twitter.com/1.1/guest/activate.json",
                headers={
                    "Authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
                    "Content-Type": "application/json",
                },
            )
            return response.json().get("guest_token")
        except Exception as e:
            print(f"Guest token error: {str(e)[:200]}")
            return None

    def scrape_tweets(self, query, max_tweets=10):
        """Hybrid scraping approach"""
        results = []

        # Method 1: Try with guest token first (most reliable)
        guest_token = self.get_guest_token()
        if guest_token:
            try:
                print("Trying API with guest token...")
                headers = {
                    "Authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
                    "x-guest-token": guest_token,
                    "Content-Type": "application/json",
                }
                params = {
                    "q": query,
                    "count": min(max_tweets, 20),
                    "tweet_mode": "extended",
                    "result_type": "recent",
                }
                response = self.session.get(
                    "https://api.twitter.com/1.1/search/tweets.json",
                    headers=headers,
                    params=params,
                    timeout=10,
                )

                if response.status_code == 200:
                    for tweet in response.json().get("statuses", []):
                        results.append(
                            {
                                "content": tweet.get("full_text", ""),
                                "username": tweet["user"]["screen_name"],
                                "date": tweet["created_at"],
                                "source": "api",
                            }
                        )
                        if len(results) >= max_tweets:
                            return results
                else:
                    print(f"API request failed with status {response.status_code}")
            except Exception as e:
                print(f"API with token failed: {str(e)[:200]}")

        # Method 2: Try mobile site
        if len(results) < max_tweets:
            try:
                print("Trying mobile site...")
                mobile_url = (
                    f"https://mobile.twitter.com/search?q={requests.utils.quote(query)}"
                )
                response = self.session.get(mobile_url, timeout=10)

                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, "html.parser")
                    tweets = soup.select('div[data-testid="tweet"]') or soup.select(
                        "div.tweet"
                    )

                    for tweet in tweets:
                        content = tweet.select_one(
                            'div[data-testid="tweetText"], div.tweet-text'
                        )
                        if content:
                            results.append(
                                {
                                    "content": content.get_text(strip=True),
                                    "source": "mobile",
                                }
                            )
                            if len(results) >= max_tweets:
                                return results
                            time.sleep(random.uniform(1, 3))
            except Exception as e:
                print(f"Mobile scrape failed: {str(e)[:200]}")

        # Method 3: Fallback to HTML scraping
        if len(results) < max_tweets:
            try:
                print("Falling back to HTML scraping...")
                html_url = f"https://twitter.com/search?q={requests.utils.quote(query)}&src=typed_query"
                response = self.session.get(html_url, timeout=10)

                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, "html.parser")
                    tweets = soup.select('article[data-testid="tweet"]')

                    for tweet in tweets:
                        content = tweet.select_one('div[data-testid="tweetText"]')
                        if content:
                            results.append(
                                {
                                    "content": content.get_text(strip=True),
                                    "source": "html",
                                }
                            )
                            if len(results) >= max_tweets:
                                break
                            time.sleep(random.uniform(2, 5))
            except Exception as e:
                print(f"HTML scrape failed: {str(e)[:200]}")

        return results


if __name__ == "__main__":
    scraper = TwitterScraperV3()
    query = "python lang:en since:2025-07-01 -filter:replies"
    max_tweets = 15  # Increased from 10

    print(f"Starting scrape for: {query}")
    tweets = scraper.scrape_tweets(query, max_tweets)

    with open("tweets.json", "w", encoding="utf-8") as f:
        json.dump(tweets, f, ensure_ascii=False, indent=2)

    print(f"Scrape completed. Found {len(tweets)} tweets.")
