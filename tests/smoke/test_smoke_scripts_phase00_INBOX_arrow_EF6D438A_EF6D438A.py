import importlib, types

def test_import_scripts_phase00_INBOX_arrow_EF6D438A_EF6D438A():
    mod = importlib.import_module("scripts.phase00.INBOX.arrow_EF6D438A_EF6D438A")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
