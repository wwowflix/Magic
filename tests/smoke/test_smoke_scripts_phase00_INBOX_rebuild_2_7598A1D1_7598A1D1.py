import importlib, types

def test_import_scripts_phase00_INBOX_rebuild_2_7598A1D1_7598A1D1():
    mod = importlib.import_module("scripts.phase00.INBOX.rebuild_2_7598A1D1_7598A1D1")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
