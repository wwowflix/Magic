import importlib, types


def test_import_scripts_phase00_INBOX_CFF2ToCFF_A6FC21EA_A6FC21EA():
    mod = importlib.import_module("scripts.phase00.INBOX.CFF2ToCFF_A6FC21EA_A6FC21EA")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
