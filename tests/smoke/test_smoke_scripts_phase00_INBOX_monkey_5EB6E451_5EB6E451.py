import importlib, types


def test_import_scripts_phase00_INBOX_monkey_5EB6E451_5EB6E451():
    mod = importlib.import_module("scripts.phase00.INBOX.monkey_5EB6E451_5EB6E451")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
