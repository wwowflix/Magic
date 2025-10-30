import importlib, types


def test_import_scripts_py34compat():
    mod = importlib.import_module("scripts.py34compat")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
