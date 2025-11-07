import importlib, types


def test_import_scripts_phase02_module_E_02E_niche_classifier_READY():
    mod = importlib.import_module("scripts.phase02.module_E.02E_niche_classifier_READY")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
