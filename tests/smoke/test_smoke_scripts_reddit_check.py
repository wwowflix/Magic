import importlib
import types


def test_import_scripts_reddit_check():
    mod = importlib.import_module("scripts.reddit_check")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
