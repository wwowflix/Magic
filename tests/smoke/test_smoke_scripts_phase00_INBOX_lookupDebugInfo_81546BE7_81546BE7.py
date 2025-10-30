import importlib, types


def test_import_scripts_phase00_INBOX_lookupDebugInfo_81546BE7_81546BE7():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.lookupDebugInfo_81546BE7_81546BE7"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
