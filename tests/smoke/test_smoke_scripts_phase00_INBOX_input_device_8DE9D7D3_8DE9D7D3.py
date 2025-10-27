import importlib, types

def test_import_scripts_phase00_INBOX_input_device_8DE9D7D3_8DE9D7D3():
    mod = importlib.import_module("scripts.phase00.INBOX.input_device_8DE9D7D3_8DE9D7D3")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
