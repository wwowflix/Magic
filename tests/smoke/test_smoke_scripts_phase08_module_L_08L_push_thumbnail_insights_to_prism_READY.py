import importlib, types


def test_import_scripts_phase08_module_L_08L_push_thumbnail_insights_to_prism_READY():
    mod = importlib.import_module(
        "scripts.phase08.module_L.08L_push_thumbnail_insights_to_prism_READY"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
