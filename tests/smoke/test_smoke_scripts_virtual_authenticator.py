import importlib, types


def test_import_scripts_virtual_authenticator():
    mod = importlib.import_module("scripts.virtual_authenticator")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
