import importlib, types

def test_import_scripts_phase00_INBOX__ufunc_config_6F76798A_6F76798A():
    mod = importlib.import_module("scripts.phase00.INBOX._ufunc_config_6F76798A_6F76798A")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
