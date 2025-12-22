"""MAGIC stub for advanced Twitter scraper.

This version is import-safe and does not perform any real network access.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class Tweet:
    username: str
    text: str
    url: str


def scrape_tweets(query: str, limit: int = 10) -> List[Tweet]:
    """Return a small list of fake tweets for testing."""
    return [
        Tweet(
            username="magic_user",
            text=f"[MAGIC stub] Tweet {i} for query={query!r}",
            url=f"https://example.com/tweets/{i}",
        )
        for i in range(min(limit, 10))
    ]


def main() -> None:
    tweets = scrape_tweets("magic")
    print(f"[MAGIC] advanced_twitter_scraper_2 stub; {len(tweets)} fake tweets generated.")


if __name__ == "__main__":
    main()
