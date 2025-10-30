import importlib, types


def test_import_scripts_phase00_INBOX_check_tables_2_9C10CBA5_9C10CBA5():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.check_tables_2_9C10CBA5_9C10CBA5"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
