import pytest


# Example scraper function stub
def example_scraper():
    # Imagine this function scrapes data and returns a list
    return ["trend1", "trend2"]


def test_scraper_returns_data():
    data = example_scraper()
    assert isinstance(data, list), "Scraper should return a list"
    assert len(data) > 0, "Scraper returned empty list"


def test_scraper_handles_empty(monkeypatch):
    # Simulate scraper returning empty list
    def empty_scraper():
        return []

    data = empty_scraper()
    assert data == [], "Empty scraper should return empty list"


def test_scraper_error_handling():
    # Simulate scraper raising exception and ensure it's caught
    with pytest.raises(Exception):
        raise Exception("Scraper error")
