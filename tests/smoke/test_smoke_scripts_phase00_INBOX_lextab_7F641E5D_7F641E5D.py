import importlib, types

def test_import_scripts_phase00_INBOX_lextab_7F641E5D_7F641E5D():
    mod = importlib.import_module("scripts.phase00.INBOX.lextab_7F641E5D_7F641E5D")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
