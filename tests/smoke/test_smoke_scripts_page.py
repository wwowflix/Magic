import importlib, types

def test_import_scripts_page():
    mod = importlib.import_module("scripts.page")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
