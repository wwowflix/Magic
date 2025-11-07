import importlib, types


def test_import_scripts_min_max_():
    mod = importlib.import_module("scripts.min_max_")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
