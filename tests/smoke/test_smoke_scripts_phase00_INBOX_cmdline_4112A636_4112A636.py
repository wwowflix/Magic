import importlib, types


def test_import_scripts_phase00_INBOX_cmdline_4112A636_4112A636():
    mod = importlib.import_module("scripts.phase00.INBOX.cmdline_4112A636_4112A636")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
