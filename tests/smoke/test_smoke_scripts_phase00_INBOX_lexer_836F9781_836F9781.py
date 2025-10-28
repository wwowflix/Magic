import importlib, types

def test_import_scripts_phase00_INBOX_lexer_836F9781_836F9781():
    mod = importlib.import_module("scripts.phase00.INBOX.lexer_836F9781_836F9781")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
