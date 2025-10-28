import importlib, types

def test_import_scripts_phase00_INBOX_cp949prober_D2329157_D2329157():
    mod = importlib.import_module("scripts.phase00.INBOX.cp949prober_D2329157_D2329157")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
