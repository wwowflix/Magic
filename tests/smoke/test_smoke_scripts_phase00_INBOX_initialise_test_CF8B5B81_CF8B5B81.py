import importlib, types


def test_import_scripts_phase00_INBOX_initialise_test_CF8B5B81_CF8B5B81():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.initialise_test_CF8B5B81_CF8B5B81"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
