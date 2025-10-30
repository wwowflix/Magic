import importlib, types


def test_import_scripts_phase00_INBOX_build_tracker_BDFF3513_BDFF3513():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.build_tracker_BDFF3513_BDFF3513"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
