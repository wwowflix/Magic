import importlib, types


def test_import_scripts_phase00_INBOX_reddit_api_3_B308E258_B308E258():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.reddit_api_3_B308E258_B308E258"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
