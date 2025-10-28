import importlib, types

def test_import_scripts__raises_group():
    mod = importlib.import_module("scripts._raises_group")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
