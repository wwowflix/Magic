import importlib, types


def test_import_scripts_phase06_module_X_06X_copyright_check_engine_READY():
    mod = importlib.import_module(
        "scripts.phase06.module_X.06X_copyright_check_engine_READY"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
