import importlib, types


def test_import_scripts_phase00_INBOX__exceptions_3_4653D197_4653D197():
    mod = importlib.import_module(
        "scripts.phase00.INBOX._exceptions_3_4653D197_4653D197"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
