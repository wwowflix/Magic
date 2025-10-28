import importlib, types

def test_import_scripts_prefs():
    mod = importlib.import_module("scripts.prefs")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
