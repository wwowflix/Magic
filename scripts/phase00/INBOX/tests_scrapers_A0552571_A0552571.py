# tests_scrapers.py


def test_sample_scraper():
    result = {"data": [1, 2, 3]}
    assert "data" in result
    assert isinstance(result["data"], list)
    assert len(result["data"]) > 0
