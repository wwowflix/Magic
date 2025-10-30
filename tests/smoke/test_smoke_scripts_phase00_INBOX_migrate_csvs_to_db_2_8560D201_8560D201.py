import importlib, types


def test_import_scripts_phase00_INBOX_migrate_csvs_to_db_2_8560D201_8560D201():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.migrate_csvs_to_db_2_8560D201_8560D201"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
