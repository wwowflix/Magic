import importlib, types


def test_import_scripts_phase00_INBOX_holiday_A1792864_A1792864():
    mod = importlib.import_module("scripts.phase00.INBOX.holiday_A1792864_A1792864")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
