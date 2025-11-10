import importlib, types


def test_import_scripts_phase00_INBOX_unistring_EA15370B_EA15370B():
    mod = importlib.import_module("scripts.phase00.INBOX.unistring_EA15370B_EA15370B")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
