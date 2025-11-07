import importlib, types


def test_import_scripts_phase00_INBOX_roundTools_D5149767_D5149767():
    mod = importlib.import_module("scripts.phase00.INBOX.roundTools_D5149767_D5149767")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
