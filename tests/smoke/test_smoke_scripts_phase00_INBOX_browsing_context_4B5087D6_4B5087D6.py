import importlib, types


def test_import_scripts_phase00_INBOX_browsing_context_4B5087D6_4B5087D6():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.browsing_context_4B5087D6_4B5087D6"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
