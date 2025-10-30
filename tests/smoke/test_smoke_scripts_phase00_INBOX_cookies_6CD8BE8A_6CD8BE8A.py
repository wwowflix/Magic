import importlib, types


def test_import_scripts_phase00_INBOX_cookies_6CD8BE8A_6CD8BE8A():
    mod = importlib.import_module("scripts.phase00.INBOX.cookies_6CD8BE8A_6CD8BE8A")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
