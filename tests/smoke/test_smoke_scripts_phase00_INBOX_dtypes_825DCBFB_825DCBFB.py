import importlib, types

def test_import_scripts_phase00_INBOX_dtypes_825DCBFB_825DCBFB():
    mod = importlib.import_module("scripts.phase00.INBOX.dtypes_825DCBFB_825DCBFB")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
