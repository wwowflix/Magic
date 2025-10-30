import importlib, types


def test_import_scripts_phase00_INBOX_to_interpreter_A170D451_A170D451():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.to_interpreter_A170D451_A170D451"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
