import importlib, types


def test_import_scripts__entry_points():
    mod = importlib.import_module("scripts._entry_points")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
