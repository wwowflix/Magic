import importlib, types


def test_import_scripts_phase01_module_A_01A_api_key_validator_READY():
    mod = importlib.import_module(
        "scripts.phase01.module_A.01A_api_key_validator_READY"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
