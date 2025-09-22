import sys
import importlib

# Allow: `from trends_scraper import ...` when module is at scripts/trends_scraper.py
try:
    mod = importlib.import_module("scripts.trends_scraper")
    sys.modules.setdefault("trends_scraper", mod)
except Exception:
    # If it truly doesn't exist, let tests decide (skip/fail) as written.
    pass

