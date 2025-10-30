import importlib, types


def test_import_scripts_phase00_INBOX_oauth_checker_2_7C7B7E75_7C7B7E75():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.oauth_checker_2_7C7B7E75_7C7B7E75"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
