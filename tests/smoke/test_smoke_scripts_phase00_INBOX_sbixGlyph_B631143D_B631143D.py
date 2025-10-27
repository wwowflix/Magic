import importlib, types

def test_import_scripts_phase00_INBOX_sbixGlyph_B631143D_B631143D():
    mod = importlib.import_module("scripts.phase00.INBOX.sbixGlyph_B631143D_B631143D")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
