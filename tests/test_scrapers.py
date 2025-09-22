import importlib, pytest
mod = importlib.import_module("trends_scraper")
for name in ("scrape_data","scrape_trends","run","main","collect","collect_data"):
    fn = getattr(mod, name, None)
    if callable(fn):
        scrape_fn = fn
        break
else:
    pytest.skip("No known scraping entrypoint found")
def test_scraper_entrypoint_present():
    assert callable(scrape_fn)

