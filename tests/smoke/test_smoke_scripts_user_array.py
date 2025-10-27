import importlib, types

def test_import_scripts_user_array():
    mod = importlib.import_module("scripts.user_array")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
