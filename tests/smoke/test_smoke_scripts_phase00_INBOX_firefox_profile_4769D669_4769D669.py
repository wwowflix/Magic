import importlib, types

def test_import_scripts_phase00_INBOX_firefox_profile_4769D669_4769D669():
    mod = importlib.import_module("scripts.phase00.INBOX.firefox_profile_4769D669_4769D669")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
