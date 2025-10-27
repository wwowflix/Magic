import importlib, types

def test_import_scripts_phase00_INBOX_defmatrix_60C6CF6A_60C6CF6A():
    mod = importlib.import_module("scripts.phase00.INBOX.defmatrix_60C6CF6A_60C6CF6A")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
