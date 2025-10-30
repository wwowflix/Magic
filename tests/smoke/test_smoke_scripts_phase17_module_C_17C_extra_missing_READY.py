import importlib, types


def test_import_scripts_phase17_module_C_17C_extra_missing_READY():
    mod = importlib.import_module("scripts.phase17.module_C.17C_extra_missing_READY")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
