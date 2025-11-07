import importlib, types


def test_import_scripts_phase00_INBOX_base_parser_EA926C73_EA926C73():
    mod = importlib.import_module("scripts.phase00.INBOX.base_parser_EA926C73_EA926C73")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
