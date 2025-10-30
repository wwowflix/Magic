import importlib, types


def test_import_scripts_phase18_module_L_18L_funnel_drop_off_analyzer_READY():
    mod = importlib.import_module(
        "scripts.phase18.module_L.18L_funnel_drop_off_analyzer_READY"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
