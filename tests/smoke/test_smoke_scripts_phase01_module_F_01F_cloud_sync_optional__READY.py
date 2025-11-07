import importlib, types


def test_import_scripts_phase01_module_F_01F_cloud_sync_optional__READY():
    mod = importlib.import_module(
        "scripts.phase01.module_F.01F_cloud_sync_optional__READY"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
