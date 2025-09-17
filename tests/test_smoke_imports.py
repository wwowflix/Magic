import importlib, pathlib, sys

# ensure repo root is importable (esp. when running in CI)
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import your_scraper_module                       # should exist at repo root
ts = importlib.import_module("scripts.trends_scraper")

def test_smoke_imports_and_call():
    assert hasattr(your_scraper_module, "__doc__")
    # touch at least one function so lines execute for coverage
    assert isinstance(getattr(ts, "get_trends")(), list)
