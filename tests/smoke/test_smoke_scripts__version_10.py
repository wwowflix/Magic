import importlib, types

def test_import_scripts__version_10():
    mod = importlib.import_module("scripts._version_10")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
