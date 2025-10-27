import importlib, types

def test_import_scripts_phase00_INBOX_subreddits_14C00938_14C00938():
    mod = importlib.import_module("scripts.phase00.INBOX.subreddits_14C00938_14C00938")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
