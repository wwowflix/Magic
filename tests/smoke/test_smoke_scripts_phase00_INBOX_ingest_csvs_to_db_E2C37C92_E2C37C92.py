import importlib, types


def test_import_scripts_phase00_INBOX_ingest_csvs_to_db_E2C37C92_E2C37C92():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.ingest_csvs_to_db_E2C37C92_E2C37C92"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
