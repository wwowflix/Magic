import importlib, types

def test_import_scripts_extension_types():
    mod = importlib.import_module("scripts.extension_types")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
