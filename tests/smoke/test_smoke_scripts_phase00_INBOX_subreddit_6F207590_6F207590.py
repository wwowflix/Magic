import importlib, types


def test_import_scripts_phase00_INBOX_subreddit_6F207590_6F207590():
    mod = importlib.import_module("scripts.phase00.INBOX.subreddit_6F207590_6F207590")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
