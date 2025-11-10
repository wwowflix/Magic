import importlib, types


def test_import_scripts_google_trends_scraper():
    mod = importlib.import_module("scripts.google_trends_scraper")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
