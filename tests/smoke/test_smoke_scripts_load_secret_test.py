import importlib, types


def test_import_scripts_load_secret_test():
    mod = importlib.import_module("scripts.load_secret_test")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
