import importlib, types


def test_import_scripts_phase00_INBOX_create_trends_table_6B09AC95_6B09AC95():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.create_trends_table_6B09AC95_6B09AC95"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
