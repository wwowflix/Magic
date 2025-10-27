import importlib, types

def test_import_scripts_phase00_INBOX_align_155EBF19_155EBF19():
    mod = importlib.import_module("scripts.phase00.INBOX.align_155EBF19_155EBF19")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
