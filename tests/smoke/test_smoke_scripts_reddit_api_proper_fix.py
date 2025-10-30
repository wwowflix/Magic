import importlib, types


def test_import_scripts_reddit_api_proper_fix():
    mod = importlib.import_module("scripts.reddit_api_proper_fix")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
