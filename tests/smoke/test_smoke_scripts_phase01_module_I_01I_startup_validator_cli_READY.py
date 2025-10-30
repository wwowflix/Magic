import importlib, types


def test_import_scripts_phase01_module_I_01I_startup_validator_cli_READY():
    mod = importlib.import_module(
        "scripts.phase01.module_I.01I_startup_validator_cli_READY"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
