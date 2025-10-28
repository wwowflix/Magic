import importlib, types

def test_import_scripts_phase11_module_I_11I_cost_overflow_stopper_READY():
    mod = importlib.import_module("scripts.phase11.module_I.11I_cost_overflow_stopper_READY")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
