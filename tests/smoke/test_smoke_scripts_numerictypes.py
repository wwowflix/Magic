import importlib, types


def test_import_scripts_numerictypes():
    mod = importlib.import_module("scripts.numerictypes")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
