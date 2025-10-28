import importlib, types

def test_import_scripts_phase00_INBOX__msvccompiler_081BA301_081BA301():
    mod = importlib.import_module("scripts.phase00.INBOX._msvccompiler_081BA301_081BA301")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
