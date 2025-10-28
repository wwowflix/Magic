import importlib, types

def test_import_scripts_phase00_INBOX_sortedset_16EADED2_16EADED2():
    mod = importlib.import_module("scripts.phase00.INBOX.sortedset_16EADED2_16EADED2")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
