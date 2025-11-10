import importlib, types


def test_import_scripts_phase00_INBOX__table_schema_0215C434_0215C434():
    mod = importlib.import_module(
        "scripts.phase00.INBOX._table_schema_0215C434_0215C434"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
