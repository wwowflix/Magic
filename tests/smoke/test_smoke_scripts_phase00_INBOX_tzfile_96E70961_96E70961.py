import importlib, types


def test_import_scripts_phase00_INBOX_tzfile_96E70961_96E70961():
    mod = importlib.import_module("scripts.phase00.INBOX.tzfile_96E70961_96E70961")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
