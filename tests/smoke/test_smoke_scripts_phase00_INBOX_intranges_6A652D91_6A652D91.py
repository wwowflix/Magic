import importlib, types


def test_import_scripts_phase00_INBOX_intranges_6A652D91_6A652D91():
    mod = importlib.import_module("scripts.phase00.INBOX.intranges_6A652D91_6A652D91")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
