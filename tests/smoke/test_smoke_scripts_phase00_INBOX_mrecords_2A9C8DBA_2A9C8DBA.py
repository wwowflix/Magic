import importlib, types


def test_import_scripts_phase00_INBOX_mrecords_2A9C8DBA_2A9C8DBA():
    mod = importlib.import_module("scripts.phase00.INBOX.mrecords_2A9C8DBA_2A9C8DBA")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
