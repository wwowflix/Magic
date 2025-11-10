import importlib, types


def test_import_scripts_phase00_INBOX_sorteddict_9C35D05E_9C35D05E():
    mod = importlib.import_module("scripts.phase00.INBOX.sorteddict_9C35D05E_9C35D05E")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
