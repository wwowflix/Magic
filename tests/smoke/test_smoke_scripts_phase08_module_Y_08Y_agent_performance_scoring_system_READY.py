import importlib, types

def test_import_scripts_phase08_module_Y_08Y_agent_performance_scoring_system_READY():
    mod = importlib.import_module("scripts.phase08.module_Y.08Y_agent_performance_scoring_system_READY")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
