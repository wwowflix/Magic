import importlib, types


def test_import_scripts_phase00_INBOX_system_info_D27526D5_D27526D5():
    mod = importlib.import_module("scripts.phase00.INBOX.system_info_D27526D5_D27526D5")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
