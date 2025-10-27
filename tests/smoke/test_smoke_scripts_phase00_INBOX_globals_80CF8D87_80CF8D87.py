import importlib, types

def test_import_scripts_phase00_INBOX_globals_80CF8D87_80CF8D87():
    mod = importlib.import_module("scripts.phase00.INBOX.globals_80CF8D87_80CF8D87")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
