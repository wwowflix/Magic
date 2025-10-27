import importlib, types

def test_import_scripts_phase00_INBOX_cu2quPen_80C53015_80C53015():
    mod = importlib.import_module("scripts.phase00.INBOX.cu2quPen_80C53015_80C53015")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
