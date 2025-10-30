import importlib, types


def test_import_scripts_phase13_module_B_13B_smart_cta_split_tester_READY():
    mod = importlib.import_module(
        "scripts.phase13.module_B.13B_smart_cta_split_tester_READY"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
