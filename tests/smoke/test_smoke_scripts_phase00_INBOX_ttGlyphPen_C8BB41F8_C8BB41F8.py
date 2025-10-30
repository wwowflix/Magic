import importlib, types


def test_import_scripts_phase00_INBOX_ttGlyphPen_C8BB41F8_C8BB41F8():
    mod = importlib.import_module("scripts.phase00.INBOX.ttGlyphPen_C8BB41F8_C8BB41F8")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
