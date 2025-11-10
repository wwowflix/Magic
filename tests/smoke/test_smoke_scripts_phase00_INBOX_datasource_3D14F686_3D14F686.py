import importlib, types


def test_import_scripts_phase00_INBOX_datasource_3D14F686_3D14F686():
    mod = importlib.import_module("scripts.phase00.INBOX.datasource_3D14F686_3D14F686")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
