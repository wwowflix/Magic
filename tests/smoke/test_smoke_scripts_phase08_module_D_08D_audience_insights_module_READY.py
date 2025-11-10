import importlib, types


def test_import_scripts_phase08_module_D_08D_audience_insights_module_READY():
    mod = importlib.import_module(
        "scripts.phase08.module_D.08D_audience_insights_module_READY"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
