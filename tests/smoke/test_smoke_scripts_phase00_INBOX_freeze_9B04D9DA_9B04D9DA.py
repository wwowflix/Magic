import importlib, types


def test_import_scripts_phase00_INBOX_freeze_9B04D9DA_9B04D9DA():
    mod = importlib.import_module("scripts.phase00.INBOX.freeze_9B04D9DA_9B04D9DA")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
