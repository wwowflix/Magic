import importlib, types

def test_import_scripts_module_with_deprecations():
    mod = importlib.import_module("scripts.module_with_deprecations")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
