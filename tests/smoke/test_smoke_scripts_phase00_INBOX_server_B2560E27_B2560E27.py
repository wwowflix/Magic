import importlib, types


def test_import_scripts_phase00_INBOX_server_B2560E27_B2560E27():
    mod = importlib.import_module("scripts.phase00.INBOX.server_B2560E27_B2560E27")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
