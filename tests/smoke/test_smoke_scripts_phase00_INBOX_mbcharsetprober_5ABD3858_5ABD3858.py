import importlib, types


def test_import_scripts_phase00_INBOX_mbcharsetprober_5ABD3858_5ABD3858():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.mbcharsetprober_5ABD3858_5ABD3858"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
