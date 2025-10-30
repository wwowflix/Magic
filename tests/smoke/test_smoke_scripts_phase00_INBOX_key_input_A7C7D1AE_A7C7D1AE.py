import importlib, types


def test_import_scripts_phase00_INBOX_key_input_A7C7D1AE_A7C7D1AE():
    mod = importlib.import_module("scripts.phase00.INBOX.key_input_A7C7D1AE_A7C7D1AE")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
