import importlib, types


def test_import_scripts_phase00_INBOX_sortedlist_9B0AA6D0_9B0AA6D0():
    mod = importlib.import_module("scripts.phase00.INBOX.sortedlist_9B0AA6D0_9B0AA6D0")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
