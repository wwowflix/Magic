import importlib, types


def test_import_scripts_phase14_module_B_14B_production_priority_queue_READY():
    mod = importlib.import_module(
        "scripts.phase14.module_B.14B_production_priority_queue_READY"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
