import importlib, types


def test_import_scripts_device_access():
    mod = importlib.import_module("scripts.device_access")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
