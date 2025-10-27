import importlib, types

def test_import_scripts_phase00_INBOX_irc_FE901301_FE901301():
    mod = importlib.import_module("scripts.phase00.INBOX.irc_FE901301_FE901301")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
