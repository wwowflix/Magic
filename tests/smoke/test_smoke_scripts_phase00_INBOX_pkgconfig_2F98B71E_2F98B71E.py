import importlib, types

def test_import_scripts_phase00_INBOX_pkgconfig_2F98B71E_2F98B71E():
    mod = importlib.import_module("scripts.phase00.INBOX.pkgconfig_2F98B71E_2F98B71E")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
