import importlib, types


def test_import_scripts_phase00_INBOX_sfnt_AE4CE729_AE4CE729():
    mod = importlib.import_module("scripts.phase00.INBOX.sfnt_AE4CE729_AE4CE729")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
