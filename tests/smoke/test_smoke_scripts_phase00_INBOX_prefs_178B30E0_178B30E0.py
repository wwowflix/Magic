import importlib, types


def test_import_scripts_phase00_INBOX_prefs_178B30E0_178B30E0():
    mod = importlib.import_module("scripts.phase00.INBOX.prefs_178B30E0_178B30E0")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
