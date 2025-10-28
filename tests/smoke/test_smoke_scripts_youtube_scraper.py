import importlib, types

def test_import_scripts_youtube_scraper():
    mod = importlib.import_module("scripts.youtube_scraper")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
