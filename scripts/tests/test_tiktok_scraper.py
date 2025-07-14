import pandas as pd

# Dummy function to simulate your TikTok scraper
def scrape_tiktok():
    data = {
        "platform": ["tiktok"],
        "title": ["Funny video"]
    }
    return pd.DataFrame(data)

def test_tiktok_returns_dataframe():
    df = scrape_tiktok()
    assert isinstance(df, pd.DataFrame)
    assert "title" in df.columns
