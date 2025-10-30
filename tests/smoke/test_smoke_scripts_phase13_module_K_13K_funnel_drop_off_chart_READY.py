import importlib, types


def test_import_scripts_phase13_module_K_13K_funnel_drop_off_chart_READY():
    mod = importlib.import_module(
        "scripts.phase13.module_K.13K_funnel_drop_off_chart_READY"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
