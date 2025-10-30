import importlib, types


def test_import_scripts_phase00_INBOX__xlsxwriter_92DF096C_92DF096C():
    mod = importlib.import_module("scripts.phase00.INBOX._xlsxwriter_92DF096C_92DF096C")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
