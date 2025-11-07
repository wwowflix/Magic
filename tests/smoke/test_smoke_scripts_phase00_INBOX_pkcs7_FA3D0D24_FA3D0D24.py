import importlib, types


def test_import_scripts_phase00_INBOX_pkcs7_FA3D0D24_FA3D0D24():
    mod = importlib.import_module("scripts.phase00.INBOX.pkcs7_FA3D0D24_FA3D0D24")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
