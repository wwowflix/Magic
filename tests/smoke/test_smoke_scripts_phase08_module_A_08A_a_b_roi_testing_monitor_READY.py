import importlib, types


def test_import_scripts_phase08_module_A_08A_a_b_roi_testing_monitor_READY():
    mod = importlib.import_module(
        "scripts.phase08.module_A.08A_a_b_roi_testing_monitor_READY"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
