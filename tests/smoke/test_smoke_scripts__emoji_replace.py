import importlib, types

def test_import_scripts__emoji_replace():
    mod = importlib.import_module("scripts._emoji_replace")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
