import importlib, types


def test_import_scripts_phase03_module_E_03E_title_roi_tuner_READY():
    mod = importlib.import_module("scripts.phase03.module_E.03E_title_roi_tuner_READY")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
