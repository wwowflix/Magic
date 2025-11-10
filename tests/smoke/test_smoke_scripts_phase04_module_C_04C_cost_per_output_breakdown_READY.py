import importlib, types


def test_import_scripts_phase04_module_C_04C_cost_per_output_breakdown_READY():
    mod = importlib.import_module(
        "scripts.phase04.module_C.04C_cost_per_output_breakdown_READY"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
