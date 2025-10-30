import importlib, types


def test_import_scripts_phase00_INBOX_lowlevel_DCB36961_DCB36961():
    mod = importlib.import_module("scripts.phase00.INBOX.lowlevel_DCB36961_DCB36961")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
