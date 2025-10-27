import importlib, types

def test_import_scripts_phase08_module_R_08R_daily_insight_generator_READY():
    mod = importlib.import_module("scripts.phase08.module_R.08R_daily_insight_generator_READY")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
