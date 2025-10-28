import importlib, types

def test_import_scripts__arrow_utils():
    mod = importlib.import_module("scripts._arrow_utils")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
