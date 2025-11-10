import importlib, types


def test_import_scripts_phase00_INBOX_ttfonts_C20AEEA9_C20AEEA9():
    mod = importlib.import_module("scripts.phase00.INBOX.ttfonts_C20AEEA9_C20AEEA9")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
