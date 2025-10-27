import importlib, types

def test_import_scripts_phase00_INBOX_standardGlyphOrder_EC063F7D_EC063F7D():
    mod = importlib.import_module("scripts.phase00.INBOX.standardGlyphOrder_EC063F7D_EC063F7D")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
