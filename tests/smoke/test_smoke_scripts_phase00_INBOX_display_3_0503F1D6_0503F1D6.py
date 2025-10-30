import importlib, types


def test_import_scripts_phase00_INBOX_display_3_0503F1D6_0503F1D6():
    mod = importlib.import_module("scripts.phase00.INBOX.display_3_0503F1D6_0503F1D6")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
