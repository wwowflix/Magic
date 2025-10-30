import importlib, types


def test_import_scripts_phase00_INBOX_table_2AE45594_2AE45594():
    mod = importlib.import_module("scripts.phase00.INBOX.table_2AE45594_2AE45594")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
