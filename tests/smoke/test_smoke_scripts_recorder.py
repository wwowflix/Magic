import importlib, types

def test_import_scripts_recorder():
    mod = importlib.import_module("scripts.recorder")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
