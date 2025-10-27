import importlib, types

def test_import_scripts_phase00_INBOX_auth_test_80E7D38A_80E7D38A():
    mod = importlib.import_module("scripts.phase00.INBOX.auth_test_80E7D38A_80E7D38A")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
