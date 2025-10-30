import importlib, types


def test_import_scripts_phase00_INBOX_check_9AE7D05F_9AE7D05F():
    mod = importlib.import_module("scripts.phase00.INBOX.check_9AE7D05F_9AE7D05F")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
