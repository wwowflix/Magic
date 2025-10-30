import importlib, types


def test_import_scripts_phase99_module_ZZ_import_error_test():
    mod = importlib.import_module("scripts.phase99.module_ZZ.import_error_test")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
