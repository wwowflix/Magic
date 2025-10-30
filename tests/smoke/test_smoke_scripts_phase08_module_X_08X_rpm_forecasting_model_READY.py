import importlib, types


def test_import_scripts_phase08_module_X_08X_rpm_forecasting_model_READY():
    mod = importlib.import_module(
        "scripts.phase08.module_X.08X_rpm_forecasting_model_READY"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
