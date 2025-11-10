import importlib, types


def test_import_scripts_phase08_module_W_08W_revenue_anomaly_detector_READY():
    mod = importlib.import_module(
        "scripts.phase08.module_W.08W_revenue_anomaly_detector_READY"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
