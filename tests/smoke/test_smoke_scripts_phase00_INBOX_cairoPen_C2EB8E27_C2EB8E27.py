import importlib, types

def test_import_scripts_phase00_INBOX_cairoPen_C2EB8E27_C2EB8E27():
    mod = importlib.import_module("scripts.phase00.INBOX.cairoPen_C2EB8E27_C2EB8E27")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
