import importlib, types


def test_import_scripts_phase00_INBOX_reddit_C4B64B92_C4B64B92():
    mod = importlib.import_module("scripts.phase00.INBOX.reddit_C4B64B92_C4B64B92")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
