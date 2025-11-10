import importlib, types


def test_import_scripts_phase00_INBOX_csvs_5A7235DB_5A7235DB():
    mod = importlib.import_module("scripts.phase00.INBOX.csvs_5A7235DB_5A7235DB")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
