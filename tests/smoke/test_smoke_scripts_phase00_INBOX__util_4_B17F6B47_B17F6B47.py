import importlib, types

def test_import_scripts_phase00_INBOX__util_4_B17F6B47_B17F6B47():
    mod = importlib.import_module("scripts.phase00.INBOX._util_4_B17F6B47_B17F6B47")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
