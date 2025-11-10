import importlib, types


def test_import_scripts_phase00_INBOX_token_DB2E0261_DB2E0261():
    mod = importlib.import_module("scripts.phase00.INBOX.token_DB2E0261_DB2E0261")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
