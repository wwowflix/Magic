import importlib, types


def test_import_scripts_phase00_INBOX_tzwin_EC0AF8BD_EC0AF8BD():
    mod = importlib.import_module("scripts.phase00.INBOX.tzwin_EC0AF8BD_EC0AF8BD")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
