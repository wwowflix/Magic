import importlib, types


def test_import_scripts_phase00_INBOX__highlevel_open_unix_stream_85A04687_85A04687():
    mod = importlib.import_module(
        "scripts.phase00.INBOX._highlevel_open_unix_stream_85A04687_85A04687"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
