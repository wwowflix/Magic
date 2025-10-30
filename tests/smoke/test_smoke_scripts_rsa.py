import importlib, types


def test_import_scripts_rsa():
    mod = importlib.import_module("scripts.rsa")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
