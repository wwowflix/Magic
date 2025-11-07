import importlib, types


def test_import_scripts_phase00_INBOX__build_tables_7D5BB750_7D5BB750():
    mod = importlib.import_module(
        "scripts.phase00.INBOX._build_tables_7D5BB750_7D5BB750"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
