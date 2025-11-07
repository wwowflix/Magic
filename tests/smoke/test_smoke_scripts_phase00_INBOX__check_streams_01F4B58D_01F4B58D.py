import importlib, types


def test_import_scripts_phase00_INBOX__check_streams_01F4B58D_01F4B58D():
    mod = importlib.import_module(
        "scripts.phase00.INBOX._check_streams_01F4B58D_01F4B58D"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
