import importlib, types


def test_import_scripts_phase00_INBOX_utils_10_6F5326FA_6F5326FA():
    mod = importlib.import_module("scripts.phase00.INBOX.utils_10_6F5326FA_6F5326FA")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
