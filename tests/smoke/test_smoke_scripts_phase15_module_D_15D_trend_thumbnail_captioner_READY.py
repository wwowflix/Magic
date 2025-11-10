import importlib, types


def test_import_scripts_phase15_module_D_15D_trend_thumbnail_captioner_READY():
    mod = importlib.import_module(
        "scripts.phase15.module_D.15D_trend_thumbnail_captioner_READY"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
