import importlib, types

def test_import_scripts_phase10_module_L_10L_platform_roi_comparer_READY():
    mod = importlib.import_module("scripts.phase10.module_L.10L_platform_roi_comparer_READY")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
