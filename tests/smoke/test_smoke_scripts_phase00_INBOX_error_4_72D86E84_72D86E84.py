import importlib, types


def test_import_scripts_phase00_INBOX_error_4_72D86E84_72D86E84():
    mod = importlib.import_module("scripts.phase00.INBOX.error_4_72D86E84_72D86E84")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
