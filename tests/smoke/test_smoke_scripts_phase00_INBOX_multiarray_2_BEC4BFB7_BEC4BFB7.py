import importlib, types


def test_import_scripts_phase00_INBOX_multiarray_2_BEC4BFB7_BEC4BFB7():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.multiarray_2_BEC4BFB7_BEC4BFB7"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
