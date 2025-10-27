import importlib, types

def test_import_scripts_phase06_module_G_06G_kpi_metrics_dashboard_generator_READY():
    mod = importlib.import_module("scripts.phase06.module_G.06G_kpi_metrics_dashboard_generator_READY")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
