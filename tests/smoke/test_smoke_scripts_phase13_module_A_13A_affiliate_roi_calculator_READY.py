import importlib, types


def test_import_scripts_phase13_module_A_13A_affiliate_roi_calculator_READY():
    mod = importlib.import_module(
        "scripts.phase13.module_A.13A_affiliate_roi_calculator_READY"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
