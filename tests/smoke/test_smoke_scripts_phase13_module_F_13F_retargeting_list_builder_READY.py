import importlib, types

def test_import_scripts_phase13_module_F_13F_retargeting_list_builder_READY():
    mod = importlib.import_module("scripts.phase13.module_F.13F_retargeting_list_builder_READY")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
