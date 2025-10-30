import importlib, types


def test_import_scripts_phase00_INBOX_ctypeslib_CCEE80E6_CCEE80E6():
    mod = importlib.import_module("scripts.phase00.INBOX.ctypeslib_CCEE80E6_CCEE80E6")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
