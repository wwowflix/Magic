import importlib, types


def test_import_scripts_phase00_INBOX__lxml_F4BE6927_F4BE6927():
    mod = importlib.import_module("scripts.phase00.INBOX._lxml_F4BE6927_F4BE6927")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
