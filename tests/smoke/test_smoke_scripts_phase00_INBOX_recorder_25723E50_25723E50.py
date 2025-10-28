import importlib, types

def test_import_scripts_phase00_INBOX_recorder_25723E50_25723E50():
    mod = importlib.import_module("scripts.phase00.INBOX.recorder_25723E50_25723E50")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
