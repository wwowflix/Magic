import importlib, types


def test_import_scripts_phase00_INBOX_shadowroot_9FAA7657_9FAA7657():
    mod = importlib.import_module("scripts.phase00.INBOX.shadowroot_9FAA7657_9FAA7657")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
