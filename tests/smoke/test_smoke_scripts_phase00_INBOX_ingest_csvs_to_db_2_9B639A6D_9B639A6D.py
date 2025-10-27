import importlib, types

def test_import_scripts_phase00_INBOX_ingest_csvs_to_db_2_9B639A6D_9B639A6D():
    mod = importlib.import_module("scripts.phase00.INBOX.ingest_csvs_to_db_2_9B639A6D_9B639A6D")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
