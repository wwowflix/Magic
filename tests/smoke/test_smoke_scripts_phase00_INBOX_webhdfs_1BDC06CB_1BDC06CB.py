import importlib, types


def test_import_scripts_phase00_INBOX_webhdfs_1BDC06CB_1BDC06CB():
    mod = importlib.import_module("scripts.phase00.INBOX.webhdfs_1BDC06CB_1BDC06CB")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
