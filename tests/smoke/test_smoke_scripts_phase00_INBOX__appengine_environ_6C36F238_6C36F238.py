import importlib, types


def test_import_scripts_phase00_INBOX__appengine_environ_6C36F238_6C36F238():
    mod = importlib.import_module(
        "scripts.phase00.INBOX._appengine_environ_6C36F238_6C36F238"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
