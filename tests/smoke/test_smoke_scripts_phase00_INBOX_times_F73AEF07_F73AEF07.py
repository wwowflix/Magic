import importlib, types


def test_import_scripts_phase00_INBOX_times_F73AEF07_F73AEF07():
    mod = importlib.import_module("scripts.phase00.INBOX.times_F73AEF07_F73AEF07")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
