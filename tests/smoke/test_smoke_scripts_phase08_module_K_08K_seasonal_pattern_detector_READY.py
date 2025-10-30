import importlib, types


def test_import_scripts_phase08_module_K_08K_seasonal_pattern_detector_READY():
    mod = importlib.import_module(
        "scripts.phase08.module_K.08K_seasonal_pattern_detector_READY"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
