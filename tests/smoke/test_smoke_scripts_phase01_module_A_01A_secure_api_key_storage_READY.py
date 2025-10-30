import importlib, types


def test_import_scripts_phase01_module_A_01A_secure_api_key_storage_READY():
    mod = importlib.import_module(
        "scripts.phase01.module_A.01A_secure_api_key_storage_READY"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
