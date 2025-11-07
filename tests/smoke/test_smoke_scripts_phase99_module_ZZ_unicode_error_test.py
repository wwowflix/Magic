import importlib
import types


def test_import_scripts_phase99_module_ZZ_unicode_error_test():
    mod = importlib.import_module("scripts.phase99.module_ZZ.unicode_error_test")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
