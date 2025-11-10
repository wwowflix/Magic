import importlib, types


def test_import_scripts_error_reporting():
    mod = importlib.import_module("scripts.error_reporting")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
