import importlib, types

def test_import_scripts_phase14_module_K_14K_smart_budget_allocator_READY():
    mod = importlib.import_module("scripts.phase14.module_K.14K_smart_budget_allocator_READY")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
