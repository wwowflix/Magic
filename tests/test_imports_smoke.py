import importlib
import pytest

# Core modules that should import everywhere
CORE_MODULES = [
    "your_scraper_module",
    "scripts.trends_scraper",
]

def test_import_core_modules():
    for mod in CORE_MODULES:
        importlib.import_module(mod)

def test_import_charts_if_plotly_present():
    # Only run this if plotly is installed; otherwise mark as skipped
    pytest.importorskip("plotly")
    importlib.import_module("scripts.charts")

