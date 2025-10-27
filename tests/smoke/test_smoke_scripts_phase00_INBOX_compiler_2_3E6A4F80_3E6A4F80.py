import importlib, types

def test_import_scripts_phase00_INBOX_compiler_2_3E6A4F80_3E6A4F80():
    mod = importlib.import_module("scripts.phase00.INBOX.compiler_2_3E6A4F80_3E6A4F80")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
