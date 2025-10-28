import importlib, types

def test_import_scripts_phase00_INBOX_mercurial_0736DDE7_0736DDE7():
    mod = importlib.import_module("scripts.phase00.INBOX.mercurial_0736DDE7_0736DDE7")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
