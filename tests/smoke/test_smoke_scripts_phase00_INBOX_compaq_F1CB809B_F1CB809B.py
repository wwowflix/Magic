import importlib, types


def test_import_scripts_phase00_INBOX_compaq_F1CB809B_F1CB809B():
    mod = importlib.import_module("scripts.phase00.INBOX.compaq_F1CB809B_F1CB809B")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
