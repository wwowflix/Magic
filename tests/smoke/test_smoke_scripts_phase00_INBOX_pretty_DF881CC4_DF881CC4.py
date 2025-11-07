import importlib, types


def test_import_scripts_phase00_INBOX_pretty_DF881CC4_DF881CC4():
    mod = importlib.import_module("scripts.phase00.INBOX.pretty_DF881CC4_DF881CC4")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
