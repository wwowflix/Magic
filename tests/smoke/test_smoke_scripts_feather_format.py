import importlib, types

def test_import_scripts_feather_format():
    mod = importlib.import_module("scripts.feather_format")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
