import importlib
import types


def test_import_scripts_phase99_module_ZZ_99Z_import_error_test_READY():
    mod = importlib.import_module(
        "scripts.phase99.module_ZZ.99Z_import_error_test_READY"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
