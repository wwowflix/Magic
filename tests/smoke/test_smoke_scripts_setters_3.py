import importlib, types

def test_import_scripts_setters_3():
    mod = importlib.import_module("scripts.setters_3")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
