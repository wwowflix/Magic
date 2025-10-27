import importlib, types

def test_import_scripts_phase00_INBOX_msvccompiler_20BD22AA_20BD22AA():
    mod = importlib.import_module("scripts.phase00.INBOX.msvccompiler_20BD22AA_20BD22AA")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
