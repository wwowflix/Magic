import importlib, types


def test_import_scripts_phase06_module_L_06L_analytics_pull_sync_READY():
    mod = importlib.import_module(
        "scripts.phase06.module_L.06L_analytics_pull_sync_READY"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
