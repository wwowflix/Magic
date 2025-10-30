import importlib, types


def test_import_scripts_exceptions_5():
    mod = importlib.import_module("scripts.exceptions_5")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
