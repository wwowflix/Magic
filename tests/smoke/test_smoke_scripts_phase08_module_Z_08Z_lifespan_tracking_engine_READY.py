import importlib, types

def test_import_scripts_phase08_module_Z_08Z_lifespan_tracking_engine_READY():
    mod = importlib.import_module("scripts.phase08.module_Z.08Z_lifespan_tracking_engine_READY")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
