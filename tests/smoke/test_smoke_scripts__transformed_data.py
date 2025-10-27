import importlib, types

def test_import_scripts__transformed_data():
    mod = importlib.import_module("scripts._transformed_data")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
