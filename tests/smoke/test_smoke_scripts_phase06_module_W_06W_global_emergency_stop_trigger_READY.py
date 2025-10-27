import importlib, types

def test_import_scripts_phase06_module_W_06W_global_emergency_stop_trigger_READY():
    mod = importlib.import_module("scripts.phase06.module_W.06W_global_emergency_stop_trigger_READY")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
