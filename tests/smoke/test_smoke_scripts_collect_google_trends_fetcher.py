import importlib, types

def test_import_scripts_collect_google_trends_fetcher():
    mod = importlib.import_module("scripts.collect.google_trends_fetcher")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
