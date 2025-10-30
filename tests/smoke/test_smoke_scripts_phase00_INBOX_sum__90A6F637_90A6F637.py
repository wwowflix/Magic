import importlib, types


def test_import_scripts_phase00_INBOX_sum__90A6F637_90A6F637():
    mod = importlib.import_module("scripts.phase00.INBOX.sum__90A6F637_90A6F637")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
