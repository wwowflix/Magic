import importlib, types

def test_import_scripts_phase00_INBOX_html_96E01590_96E01590():
    mod = importlib.import_module("scripts.phase00.INBOX.html_96E01590_96E01590")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
