import importlib, types


def test_import_scripts_phase06_module_N_06N_notion_performance_sync_READY():
    mod = importlib.import_module(
        "scripts.phase06.module_N.06N_notion_performance_sync_READY"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
