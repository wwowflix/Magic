import importlib, types


def test_import_scripts_phase08_module_O_08O_funnel_roi_traceback_engine_READY():
    mod = importlib.import_module(
        "scripts.phase08.module_O.08O_funnel_roi_traceback_engine_READY"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
