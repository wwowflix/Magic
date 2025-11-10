import importlib, types


def test_import_scripts_phase00_INBOX_check_notion_csv_D574CD47_D574CD47():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.check_notion_csv_D574CD47_D574CD47"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
