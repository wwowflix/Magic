import importlib, types

def test_import_scripts_phase00_INBOX_reddit_check_EFBE0BD1_EFBE0BD1():
    mod = importlib.import_module("scripts.phase00.INBOX.reddit_check_EFBE0BD1_EFBE0BD1")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
