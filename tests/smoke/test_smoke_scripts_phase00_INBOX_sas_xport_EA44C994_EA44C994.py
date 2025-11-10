import importlib, types


def test_import_scripts_phase00_INBOX_sas_xport_EA44C994_EA44C994():
    mod = importlib.import_module("scripts.phase00.INBOX.sas_xport_EA44C994_EA44C994")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
