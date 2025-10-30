import importlib, types


def test_import_scripts_phase00_INBOX_reddit_api_proper_fix_971E0D4C_971E0D4C():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.reddit_api_proper_fix_971E0D4C_971E0D4C"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
