import importlib, types


def test_import_scripts_phase00_INBOX_init_db_2_BEA113D7_BEA113D7():
    mod = importlib.import_module("scripts.phase00.INBOX.init_db_2_BEA113D7_BEA113D7")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
