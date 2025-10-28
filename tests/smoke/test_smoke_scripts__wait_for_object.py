import importlib, types

def test_import_scripts__wait_for_object():
    mod = importlib.import_module("scripts._wait_for_object")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
