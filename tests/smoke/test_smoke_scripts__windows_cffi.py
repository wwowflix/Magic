import importlib, types

def test_import_scripts__windows_cffi():
    mod = importlib.import_module("scripts._windows_cffi")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
