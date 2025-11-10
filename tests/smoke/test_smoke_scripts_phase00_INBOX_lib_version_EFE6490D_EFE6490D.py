import importlib, types


def test_import_scripts_phase00_INBOX_lib_version_EFE6490D_EFE6490D():
    mod = importlib.import_module("scripts.phase00.INBOX.lib_version_EFE6490D_EFE6490D")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
