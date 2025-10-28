import importlib, types

def test_import_scripts_interpolate_layout():
    mod = importlib.import_module("scripts.interpolate_layout")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
