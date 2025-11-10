import importlib, types


def test_import_scripts_phase00_INBOX_groupby_C50AFD76_C50AFD76():
    mod = importlib.import_module("scripts.phase00.INBOX.groupby_C50AFD76_C50AFD76")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
