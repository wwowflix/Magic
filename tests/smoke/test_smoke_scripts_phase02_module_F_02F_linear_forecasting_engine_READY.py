import importlib, types

def test_import_scripts_phase02_module_F_02F_linear_forecasting_engine_READY():
    mod = importlib.import_module("scripts.phase02.module_F.02F_linear_forecasting_engine_READY")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
