import importlib, types


def test_import_scripts_phase11_module_Z_11Z_step_by_step_time_travel_debugger_READY():
    mod = importlib.import_module(
        "scripts.phase11.module_Z.11Z_step_by_step_time_travel_debugger_READY"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
