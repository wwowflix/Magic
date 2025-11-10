import importlib, types


def test_import_scripts_phase00_INBOX_dir_util_CEB3FE30_CEB3FE30():
    mod = importlib.import_module("scripts.phase00.INBOX.dir_util_CEB3FE30_CEB3FE30")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
