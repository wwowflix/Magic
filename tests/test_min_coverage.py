import importlib, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import your_scraper_module as y
ts = importlib.import_module("scripts.trends_scraper")

def test_min_coverage():
    assert y.ping() == "pong"
    trends = ts.get_trends()
    assert isinstance(trends, list) and len(trends) >= 1
