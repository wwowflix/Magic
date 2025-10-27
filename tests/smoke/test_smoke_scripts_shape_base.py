import importlib, types

def test_import_scripts_shape_base():
    mod = importlib.import_module("scripts.shape_base")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
