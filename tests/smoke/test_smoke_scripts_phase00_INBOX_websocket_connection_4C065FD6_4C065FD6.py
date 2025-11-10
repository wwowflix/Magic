import importlib, types


def test_import_scripts_phase00_INBOX_websocket_connection_4C065FD6_4C065FD6():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.websocket_connection_4C065FD6_4C065FD6"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
