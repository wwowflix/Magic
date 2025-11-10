import importlib, types


def test_import_scripts_phase00_INBOX_tornadoweb_2BA0F898_2BA0F898():
    mod = importlib.import_module("scripts.phase00.INBOX.tornadoweb_2BA0F898_2BA0F898")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
