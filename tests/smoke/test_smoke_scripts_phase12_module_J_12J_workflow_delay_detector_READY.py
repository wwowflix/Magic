import importlib, types


def test_import_scripts_phase12_module_J_12J_workflow_delay_detector_READY():
    mod = importlib.import_module(
        "scripts.phase12.module_J.12J_workflow_delay_detector_READY"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
