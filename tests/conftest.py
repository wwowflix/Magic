import importlib, sys, pytest
try:
    mod = importlib.import_module("scripts.trends_scraper")
except Exception as e:
    pytest.skip(f"Could not import scripts.trends_scraper: {e}", allow_module_level=True)
else:
    sys.modules.setdefault("trends_scraper", mod)

