import importlib, types


def test_import_scripts_phase00_INBOX_import_error_test_669F2A56_669F2A56():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.import_error_test_669F2A56_669F2A56"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
