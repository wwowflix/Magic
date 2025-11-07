import importlib, types


def test_import_scripts__deprecation_warning():
    mod = importlib.import_module("scripts._deprecation_warning")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
