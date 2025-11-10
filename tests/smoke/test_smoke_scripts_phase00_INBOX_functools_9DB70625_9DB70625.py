import importlib, types


def test_import_scripts_phase00_INBOX_functools_9DB70625_9DB70625():
    mod = importlib.import_module("scripts.phase00.INBOX.functools_9DB70625_9DB70625")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
