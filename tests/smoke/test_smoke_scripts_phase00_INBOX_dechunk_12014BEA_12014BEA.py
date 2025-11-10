import importlib, types


def test_import_scripts_phase00_INBOX_dechunk_12014BEA_12014BEA():
    mod = importlib.import_module("scripts.phase00.INBOX.dechunk_12014BEA_12014BEA")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
