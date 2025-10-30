import importlib, types


def test_import_scripts_setitem():
    mod = importlib.import_module("scripts.setitem")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
