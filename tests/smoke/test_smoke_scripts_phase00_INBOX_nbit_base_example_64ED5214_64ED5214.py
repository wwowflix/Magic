import importlib, types

def test_import_scripts_phase00_INBOX_nbit_base_example_64ED5214_64ED5214():
    mod = importlib.import_module("scripts.phase00.INBOX.nbit_base_example_64ED5214_64ED5214")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
