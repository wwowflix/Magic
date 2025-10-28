import importlib, types

def test_import_scripts_phase08_module_N_08N_instagram_analytics_sync_READY():
    mod = importlib.import_module("scripts.phase08.module_N.08N_instagram_analytics_sync_READY")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
