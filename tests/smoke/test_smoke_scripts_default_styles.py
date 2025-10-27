import importlib, types

def test_import_scripts_default_styles():
    mod = importlib.import_module("scripts.default_styles")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
