import importlib, types


def test_import_scripts_phase00_INBOX_simple_py3_1EE2EB73_1EE2EB73():
    mod = importlib.import_module("scripts.phase00.INBOX.simple_py3_1EE2EB73_1EE2EB73")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
