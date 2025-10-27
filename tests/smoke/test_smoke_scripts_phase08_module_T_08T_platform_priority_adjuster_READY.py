import importlib, types

def test_import_scripts_phase08_module_T_08T_platform_priority_adjuster_READY():
    mod = importlib.import_module("scripts.phase08.module_T.08T_platform_priority_adjuster_READY")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
