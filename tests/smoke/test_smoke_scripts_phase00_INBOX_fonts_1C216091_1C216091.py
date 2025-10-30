import importlib, types


def test_import_scripts_phase00_INBOX_fonts_1C216091_1C216091():
    mod = importlib.import_module("scripts.phase00.INBOX.fonts_1C216091_1C216091")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
