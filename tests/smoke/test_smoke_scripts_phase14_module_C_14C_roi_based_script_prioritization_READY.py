import importlib, types

def test_import_scripts_phase14_module_C_14C_roi_based_script_prioritization_READY():
    mod = importlib.import_module("scripts.phase14.module_C.14C_roi_based_script_prioritization_READY")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
