import importlib, types

def test_import_scripts_phase00_INBOX_get_version_97B26E60_97B26E60():
    mod = importlib.import_module("scripts.phase00.INBOX.get_version_97B26E60_97B26E60")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
