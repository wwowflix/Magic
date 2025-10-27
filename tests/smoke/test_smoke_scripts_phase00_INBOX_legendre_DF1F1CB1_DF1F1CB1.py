import importlib, types

def test_import_scripts_phase00_INBOX_legendre_DF1F1CB1_DF1F1CB1():
    mod = importlib.import_module("scripts.phase00.INBOX.legendre_DF1F1CB1_DF1F1CB1")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
