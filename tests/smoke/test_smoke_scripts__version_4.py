import importlib, types

def test_import_scripts__version_4():
    mod = importlib.import_module("scripts._version_4")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
