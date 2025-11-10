import importlib, types


def test_import_scripts_phase00_INBOX_core_10_D6D2DCB7_D6D2DCB7():
    mod = importlib.import_module("scripts.phase00.INBOX.core_10_D6D2DCB7_D6D2DCB7")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
