import importlib
import types


def test_import_scripts_trends_scraper_with_reddit():
    mod = importlib.import_module("scripts.trends_scraper_with_reddit")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
