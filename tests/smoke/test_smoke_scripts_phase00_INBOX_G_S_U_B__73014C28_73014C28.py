import importlib, types


def test_import_scripts_phase00_INBOX_G_S_U_B__73014C28_73014C28():
    mod = importlib.import_module("scripts.phase00.INBOX.G_S_U_B__73014C28_73014C28")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
