import importlib, types


def test_import_scripts_phase13_module_G_13G_duplicate_click_filter_READY():
    mod = importlib.import_module(
        "scripts.phase13.module_G.13G_duplicate_click_filter_READY"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
