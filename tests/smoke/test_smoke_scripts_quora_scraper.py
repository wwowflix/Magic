import importlib, types


def test_import_scripts_quora_scraper():
    mod = importlib.import_module("scripts.quora_scraper")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
