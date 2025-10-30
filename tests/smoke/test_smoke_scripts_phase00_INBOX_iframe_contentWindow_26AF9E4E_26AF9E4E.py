import importlib, types


def test_import_scripts_phase00_INBOX_iframe_contentWindow_26AF9E4E_26AF9E4E():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.iframe_contentWindow_26AF9E4E_26AF9E4E"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
