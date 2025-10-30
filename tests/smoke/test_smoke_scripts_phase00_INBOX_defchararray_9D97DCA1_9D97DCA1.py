import importlib, types


def test_import_scripts_phase00_INBOX_defchararray_9D97DCA1_9D97DCA1():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.defchararray_9D97DCA1_9D97DCA1"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
