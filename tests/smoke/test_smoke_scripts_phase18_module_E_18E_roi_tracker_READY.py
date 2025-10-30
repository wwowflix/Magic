import importlib, types


def test_import_scripts_phase18_module_E_18E_roi_tracker_READY():
    mod = importlib.import_module("scripts.phase18.module_E.18E_roi_tracker_READY")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
