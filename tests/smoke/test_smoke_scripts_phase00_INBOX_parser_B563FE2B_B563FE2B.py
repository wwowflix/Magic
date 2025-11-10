import importlib, types


def test_import_scripts_phase00_INBOX_parser_B563FE2B_B563FE2B():
    mod = importlib.import_module("scripts.phase00.INBOX.parser_B563FE2B_B563FE2B")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
