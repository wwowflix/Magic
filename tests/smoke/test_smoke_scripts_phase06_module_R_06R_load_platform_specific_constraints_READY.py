import importlib, types


def test_import_scripts_phase06_module_R_06R_load_platform_specific_constraints_READY():
    mod = importlib.import_module(
        "scripts.phase06.module_R.06R_load_platform_specific_constraints_READY"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
