import importlib, types

def test_import_scripts_phase00_INBOX_reorderGlyphs_4DBC4BC6_4DBC4BC6():
    mod = importlib.import_module("scripts.phase00.INBOX.reorderGlyphs_4DBC4BC6_4DBC4BC6")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
