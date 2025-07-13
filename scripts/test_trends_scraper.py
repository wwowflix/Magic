from trends_scraper import TrendsScraper

def test_scraper():
    scraper = TrendsScraper()
    df = scraper.scrape_google_trends(["Python", "AI"])

    assert df is not None, "Scraper returned no data"
    assert not df.empty, "DataFrame is empty"
    assert "keyword" in df.columns
    assert "platform" in df.columns

    print("✅ test_trends_scraper.py passed.")

if __name__ == "__main__":
    test_scraper()
