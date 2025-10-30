import importlib, types


def test_import_scripts_phase05_module_D_05D_highlight_to_short_extractor_READY():
    mod = importlib.import_module(
        "scripts.phase05.module_D.05D_highlight_to_short_extractor_READY"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
