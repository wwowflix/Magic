import importlib, types


def test_import_scripts_phase00_INBOX_appdirs_F2492C03_F2492C03():
    mod = importlib.import_module("scripts.phase00.INBOX.appdirs_F2492C03_F2492C03")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
