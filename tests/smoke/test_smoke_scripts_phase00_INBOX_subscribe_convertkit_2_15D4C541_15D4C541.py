import importlib, types


def test_import_scripts_phase00_INBOX_subscribe_convertkit_2_15D4C541_15D4C541():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.subscribe_convertkit_2_15D4C541_15D4C541"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
