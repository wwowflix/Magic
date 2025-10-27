import importlib, types

def test_import_scripts_filepost():
    mod = importlib.import_module("scripts.filepost")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
