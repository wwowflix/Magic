import importlib, types


def test_import_scripts_phase00_INBOX_inspect_columns_2_7FA22165_7FA22165():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.inspect_columns_2_7FA22165_7FA22165"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
