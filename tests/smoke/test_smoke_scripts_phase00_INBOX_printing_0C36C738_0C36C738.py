import importlib, types


def test_import_scripts_phase00_INBOX_printing_0C36C738_0C36C738():
    mod = importlib.import_module("scripts.phase00.INBOX.printing_0C36C738_0C36C738")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
