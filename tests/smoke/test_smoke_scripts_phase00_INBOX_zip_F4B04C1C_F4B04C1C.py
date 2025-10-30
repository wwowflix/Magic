import importlib, types


def test_import_scripts_phase00_INBOX_zip_F4B04C1C_F4B04C1C():
    mod = importlib.import_module("scripts.phase00.INBOX.zip_F4B04C1C_F4B04C1C")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
