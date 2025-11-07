import importlib, types


def test_import_scripts_phase00_INBOX_css_parser_CA6F721E_CA6F721E():
    mod = importlib.import_module("scripts.phase00.INBOX.css_parser_CA6F721E_CA6F721E")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
