import importlib, types


def test_import_scripts_phase15_module_B_15B_peak_engagement_prediction_READY():
    mod = importlib.import_module(
        "scripts.phase15.module_B.15B_peak_engagement_prediction_READY"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
