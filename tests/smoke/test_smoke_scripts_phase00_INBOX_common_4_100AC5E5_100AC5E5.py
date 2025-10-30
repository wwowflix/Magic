import importlib, types


def test_import_scripts_phase00_INBOX_common_4_100AC5E5_100AC5E5():
    mod = importlib.import_module("scripts.phase00.INBOX.common_4_100AC5E5_100AC5E5")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
