import importlib, types

def test_import_scripts_phase00_INBOX_termui_BC062B28_BC062B28():
    mod = importlib.import_module("scripts.phase00.INBOX.termui_BC062B28_BC062B28")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
