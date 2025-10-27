import importlib, types

def test_import_scripts_extra_validations():
    mod = importlib.import_module("scripts.extra_validations")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
