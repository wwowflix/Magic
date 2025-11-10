import importlib, types


def test_import_scripts_low_level():
    mod = importlib.import_module("scripts.low_level")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
