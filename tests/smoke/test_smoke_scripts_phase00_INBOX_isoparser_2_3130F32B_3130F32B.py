import importlib, types


def test_import_scripts_phase00_INBOX_isoparser_2_3130F32B_3130F32B():
    mod = importlib.import_module("scripts.phase00.INBOX.isoparser_2_3130F32B_3130F32B")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
