import importlib, types


def test_import_scripts_phase00_INBOX_parser_4_F13EA890_F13EA890():
    mod = importlib.import_module("scripts.phase00.INBOX.parser_4_F13EA890_F13EA890")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
