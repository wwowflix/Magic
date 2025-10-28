import importlib, types

def test_import_scripts_phase00_INBOX_T_S_I_P__B6381297_B6381297():
    mod = importlib.import_module("scripts.phase00.INBOX.T_S_I_P__B6381297_B6381297")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
