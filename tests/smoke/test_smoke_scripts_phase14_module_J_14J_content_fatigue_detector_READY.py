import importlib, types

def test_import_scripts_phase14_module_J_14J_content_fatigue_detector_READY():
    mod = importlib.import_module("scripts.phase14.module_J.14J_content_fatigue_detector_READY")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
