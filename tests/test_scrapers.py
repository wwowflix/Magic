import pytest
from trends_scraper import scrape_data

def test_scrape_empty_result(monkeypatch):
    monkeypatch.setattr('your_scraper_module.network_call', lambda: [])
    result = scrape_data()
    assert result == [], 'Scraper should return empty list on no data'

def test_scrape_network_error(monkeypatch):
    def raise_error():
        raise Exception('Network error')
    monkeypatch.setattr('your_scraper_module.network_call', raise_error)
    with pytest.raises(Exception):
        scrape_data()

def test_scrape_valid_data():
    result = scrape_data()
    assert isinstance(result, list), 'Result should be a list'
    assert all(isinstance(item, dict) for item in result), 'All items should be dicts'
    assert 'title' in result[0], 'Each item should have a title'

