import importlib, types


def test_import_scripts_x963kdf():
    mod = importlib.import_module("scripts.x963kdf")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
