import importlib, types

def test_import_scripts_ipython():
    mod = importlib.import_module("scripts.ipython")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
