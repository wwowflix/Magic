import importlib, types


def test_import_scripts_check_type_completeness():
    mod = importlib.import_module("scripts.check_type_completeness")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
