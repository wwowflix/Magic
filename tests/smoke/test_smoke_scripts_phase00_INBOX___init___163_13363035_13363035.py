import importlib, types


def test_import_scripts_phase00_INBOX___init___163_13363035_13363035():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.__init___163_13363035_13363035"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
