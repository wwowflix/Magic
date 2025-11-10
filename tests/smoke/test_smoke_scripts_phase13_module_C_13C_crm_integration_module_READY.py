import importlib, types


def test_import_scripts_phase13_module_C_13C_crm_integration_module_READY():
    mod = importlib.import_module(
        "scripts.phase13.module_C.13C_crm_integration_module_READY"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
