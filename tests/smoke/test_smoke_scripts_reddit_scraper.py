import importlib
import types


def test_import_scripts_reddit_scraper():
    mod = importlib.import_module("scripts.reddit_scraper")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
