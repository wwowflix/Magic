import importlib, types


def test_import_scripts_phase00_INBOX_database_1433D0EF_1433D0EF():
    mod = importlib.import_module("scripts.phase00.INBOX.database_1433D0EF_1433D0EF")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
