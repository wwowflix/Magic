import importlib, types

def test_import_scripts_phase00_INBOX_S_T_A_T__CBD36258_CBD36258():
    mod = importlib.import_module("scripts.phase00.INBOX.S_T_A_T__CBD36258_CBD36258")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
