import importlib, types

def test_import_scripts_phase00_INBOX_specializer_BEC38F91_BEC38F91():
    mod = importlib.import_module("scripts.phase00.INBOX.specializer_BEC38F91_BEC38F91")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
