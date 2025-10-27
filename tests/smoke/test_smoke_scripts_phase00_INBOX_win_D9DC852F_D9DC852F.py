import importlib, types

def test_import_scripts_phase00_INBOX_win_D9DC852F_D9DC852F():
    mod = importlib.import_module("scripts.phase00.INBOX.win_D9DC852F_D9DC852F")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
