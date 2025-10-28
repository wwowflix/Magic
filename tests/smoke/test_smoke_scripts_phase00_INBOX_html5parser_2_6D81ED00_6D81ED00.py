import importlib, types

def test_import_scripts_phase00_INBOX_html5parser_2_6D81ED00_6D81ED00():
    mod = importlib.import_module("scripts.phase00.INBOX.html5parser_2_6D81ED00_6D81ED00")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
