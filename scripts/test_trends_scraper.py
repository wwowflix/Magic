import pytest
from trends_scraper import TrendsScraper

def test_scrape_returns_topics():
    scraper = TrendsScraper()
    topics = scraper.scrape()
    assert isinstance(topics, list)
    assert all(isinstance(topic, str) and topic for topic in topics)
