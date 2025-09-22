import importlib, pytest
mod = importlib.import_module("trends_scraper")
TrendsScraper = getattr(mod, "TrendsScraper", None)

@pytest.mark.skipif(TrendsScraper is None, reason="No TrendsScraper class in module")
def test_trends_scraper_has_entrypoint():
    # Don’t instantiate (constructor could need args); just require a usable entrypoint.
    assert any(hasattr(TrendsScraper, n) for n in ("run", "__call__", "main"))

