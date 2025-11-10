import importlib, types


def test_import_scripts_phase00_INBOX_html5parser_37D3FEB0_37D3FEB0():
    mod = importlib.import_module("scripts.phase00.INBOX.html5parser_37D3FEB0_37D3FEB0")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
