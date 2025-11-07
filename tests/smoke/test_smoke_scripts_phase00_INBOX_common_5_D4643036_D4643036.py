import importlib, types


def test_import_scripts_phase00_INBOX_common_5_D4643036_D4643036():
    mod = importlib.import_module("scripts.phase00.INBOX.common_5_D4643036_D4643036")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
