import importlib, types

def test_import_scripts_phase00_INBOX_ingest_test_8CFD79FA_8CFD79FA():
    mod = importlib.import_module("scripts.phase00.INBOX.ingest_test_8CFD79FA_8CFD79FA")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
