import importlib, types

def test_import_scripts_phase15_module_G_15G_negative_feedback_blocker_READY():
    mod = importlib.import_module("scripts.phase15.module_G.15G_negative_feedback_blocker_READY")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
