import importlib, types


def test_import_scripts_phase00_INBOX_dbfs_2F6A9765_2F6A9765():
    mod = importlib.import_module("scripts.phase00.INBOX.dbfs_2F6A9765_2F6A9765")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
