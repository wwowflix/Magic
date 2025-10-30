import importlib, types


def test_import_scripts_phase06_module_J_06J_caption_translator_READY():
    mod = importlib.import_module(
        "scripts.phase06.module_J.06J_caption_translator_READY"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
