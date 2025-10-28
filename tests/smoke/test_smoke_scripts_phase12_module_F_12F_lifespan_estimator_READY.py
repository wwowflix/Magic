import importlib, types

def test_import_scripts_phase12_module_F_12F_lifespan_estimator_READY():
    mod = importlib.import_module("scripts.phase12.module_F.12F_lifespan_estimator_READY")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
